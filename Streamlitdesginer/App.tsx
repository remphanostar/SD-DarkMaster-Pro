import React, { useState, useCallback } from 'react';
import type { CanvasComponent } from './types';
import { STREAMLIT_COMPONENTS } from './constants';
import Sidebar from './components/Sidebar';
import Canvas from './components/Canvas';
import PropertiesPanel from './components/PropertiesPanel';
import CodeOutput from './components/CodeOutput';
import { parseStreamlitCode } from './services/codeParser';

enum RightPanelTab {
    PROPERTIES,
    CODE
}

const recursivelyFindAndUpdate = (
    components: CanvasComponent[],
    id: string,
    updater: (c: CanvasComponent) => CanvasComponent
): CanvasComponent[] => {
    return components.map(c => {
        if (c.id === id) {
            return updater(c);
        }
        if (c.children) {
            return {
                ...c,
                children: c.children.map(col => recursivelyFindAndUpdate(col, id, updater)),
            };
        }
        return c;
    });
};

const recursivelyFindAndDelete = (
    components: CanvasComponent[],
    id: string
): CanvasComponent[] => {
    const newComponents = components.filter(c => c.id !== id);
    return newComponents.map(c => {
        if (c.children) {
            return {
                ...c,
                children: c.children.map(col => recursivelyFindAndDelete(col, id)),
            };
        }
        return c;
    });
};

const findComponentById = (components: CanvasComponent[], id: string): CanvasComponent | null => {
    for (const component of components) {
        if (component.id === id) {
            return component;
        }
        if (component.children) {
            for (const col of component.children) {
                const found = findComponentById(col, id);
                if (found) return found;
            }
        }
    }
    return null;
}


const App: React.FC = () => {
    const [canvasComponents, setCanvasComponents] = useState<CanvasComponent[]>([]);
    const [selectedComponentId, setSelectedComponentId] = useState<string | null>(null);
    const [activeTab, setActiveTab] = useState<RightPanelTab>(RightPanelTab.PROPERTIES);

    const handleDragStart = useCallback((e: React.DragEvent<HTMLDivElement>, componentType: string) => {
        e.dataTransfer.setData('componentType', componentType);
    }, []);

    const addComponent = useCallback((componentType: string, parentId?: string, columnIndex?: number) => {
        const componentDef = STREAMLIT_COMPONENTS[componentType];
        if (!componentDef) return;

        const newComponent: CanvasComponent = {
            id: `${componentType}-${Date.now()}`,
            type: componentType,
            props: Object.fromEntries(
                componentDef.properties.map(p => [p.name, p.defaultValue])
            ),
        };

        if (componentType === 'columns') {
            const spec = (newComponent.props.spec as string).split(',');
            newComponent.children = Array.from({ length: spec.length }, () => []);
        } else if (['expander', 'container', 'form'].includes(componentType)) {
            newComponent.children = [[]];
        } else if (componentType === 'tabs') {
            const labels = (newComponent.props.labels as string).split(',');
            newComponent.children = Array.from({ length: labels.length }, () => []);
        }


        if (parentId !== undefined && columnIndex !== undefined) {
            setCanvasComponents(prev =>
                recursivelyFindAndUpdate(prev, parentId, parent => {
                    const newChildren = [...(parent.children || [])];
                    if (!newChildren[columnIndex]) newChildren[columnIndex] = [];
                    newChildren[columnIndex].push(newComponent);
                    return { ...parent, children: newChildren };
                })
            );
        } else {
            setCanvasComponents(prev => [...prev, newComponent]);
        }
        setSelectedComponentId(newComponent.id);
        setActiveTab(RightPanelTab.PROPERTIES);
    }, []);

    const handleDrop = useCallback((e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
        const componentType = e.dataTransfer.getData('componentType');
        if (componentType) {
            addComponent(componentType);
        }
    }, [addComponent]);

    const handleDropInColumn = useCallback((e: React.DragEvent<HTMLDivElement>, parentId: string, columnIndex: number) => {
        e.preventDefault();
        e.stopPropagation();
        const componentType = e.dataTransfer.getData('componentType');
        if (componentType) {
            addComponent(componentType, parentId, columnIndex);
        }
    }, [addComponent]);

    const handleDragOver = useCallback((e: React.DragEvent<HTMLDivElement>) => {
        e.preventDefault();
    }, []);
    
    const handleSelectComponent = useCallback((id: string) => {
        setSelectedComponentId(id);
        if (id) {
            setActiveTab(RightPanelTab.PROPERTIES);
        }
    }, []);

    const handleDeleteComponent = useCallback((id: string) => {
        setCanvasComponents(prev => recursivelyFindAndDelete(prev, id));
        if (selectedComponentId === id) {
            setSelectedComponentId(null);
        }
    }, [selectedComponentId]);
    
    const handleUpdateComponent = useCallback((id: string, newProps: { [key: string]: any }) => {
        setCanvasComponents(prev => 
            recursivelyFindAndUpdate(prev, id, c => {
                const updatedComponent = { ...c, props: newProps };

                if (c.type === 'columns' && newProps.spec !== c.props.spec) {
                    const newSpec = (newProps.spec as string || '1,1').split(',').map(s => s.trim()).filter(Boolean);
                    const newCount = newSpec.length;
                    if (newCount > 0 && newCount <= 20) { // Limit columns
                        const oldChildren = c.children || [];
                        const newChildren = Array.from({ length: newCount }, (_, i) => oldChildren[i] || []);
                        updatedComponent.children = newChildren;
                    }
                } else if (c.type === 'tabs' && newProps.labels !== c.props.labels) {
                    const newLabels = (newProps.labels as string || '').split(',');
                    const newCount = newLabels.length;
                     if (newCount > 0) {
                        const oldChildren = c.children || [];
                        const newChildren = Array.from({ length: newCount }, (_, i) => oldChildren[i] || []);
                        updatedComponent.children = newChildren;
                    }
                }

                return updatedComponent;
            })
        );
    }, []);

    const handleCodeUpdate = useCallback((newCode: string) => {
        try {
            const newComponents = parseStreamlitCode(newCode);
            setCanvasComponents(newComponents);
            setSelectedComponentId(null);
        } catch (error) {
            console.error("Failed to parse code:", error);
            alert("Error parsing code. Please check the format. This feature works best with code generated by this tool.");
        }
    }, []);

    const selectedComponent = selectedComponentId ? findComponentById(canvasComponents, selectedComponentId) : null;

    return (
        <div className="flex h-screen w-screen bg-dark-bg font-sans">
            <Sidebar onDragStart={handleDragStart} />
            <Canvas
                components={canvasComponents}
                selectedComponentId={selectedComponentId}
                onDrop={handleDrop}
                onDropInColumn={handleDropInColumn}
                onDragOver={handleDragOver}
                onSelectComponent={handleSelectComponent}
                onDeleteComponent={handleDeleteComponent}
            />
            <aside className="w-96 bg-dark-card border-l border-dark-border flex flex-col">
                <div className="flex border-b border-dark-border">
                    <button 
                        onClick={() => setActiveTab(RightPanelTab.PROPERTIES)}
                        className={`flex-1 p-3 font-semibold ${activeTab === RightPanelTab.PROPERTIES ? 'bg-dark-border text-streamlit-red' : 'text-dark-text-light hover:bg-dark-border/50'}`}
                    >
                        Properties
                    </button>
                    <button 
                        onClick={() => setActiveTab(RightPanelTab.CODE)}
                        className={`flex-1 p-3 font-semibold ${activeTab === RightPanelTab.CODE ? 'bg-dark-border text-streamlit-red' : 'text-dark-text-light hover:bg-dark-border/50'}`}
                    >
                        Code
                    </button>
                </div>
                <div className="flex-grow overflow-auto">
                    {activeTab === RightPanelTab.PROPERTIES ? (
                        <PropertiesPanel
                            selectedComponent={selectedComponent}
                            onUpdateComponent={handleUpdateComponent}
                        />
                    ) : (
                        <CodeOutput components={canvasComponents} onUpdateCanvas={handleCodeUpdate} />
                    )}
                </div>
            </aside>
        </div>
    );
};

export default App;