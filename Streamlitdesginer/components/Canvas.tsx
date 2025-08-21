import React, { useState } from 'react';
import type { CanvasComponent } from '../types';

const TrashIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" /></svg>;

// Icons for placeholders
const ImageIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>;
const AudioIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.858 5.858a3 3 0 104.243 4.243L5.858 14.343a3 3 0 00-4.243-4.243l4.243-4.243z" /></svg>;
const VideoIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-gray-500" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>;
const InfoIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-2" viewBox="0 0 20 20" fill="currentColor"><path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd" /></svg>;


interface CanvasProps {
    components: CanvasComponent[];
    selectedComponentId: string | null;
    onDrop: (e: React.DragEvent<HTMLDivElement>) => void;
    onDropInColumn: (e: React.DragEvent<HTMLDivElement>, parentId: string, columnIndex: number) => void;
    onDragOver: (e: React.DragEvent<HTMLDivElement>) => void;
    onSelectComponent: (id: string) => void;
    onDeleteComponent: (id: string) => void;
}

const ComponentRenderer: React.FC<Omit<CanvasProps, 'components' | 'onDrop'> & { component: CanvasComponent }> = ({
    component,
    selectedComponentId,
    onDropInColumn,
    onDragOver,
    onSelectComponent,
    onDeleteComponent,
}) => {
    const { type, props } = component;
    const commonInputLabelClasses = "text-sm text-dark-text-light block mb-1";
    const commonInputClasses = "w-full p-2 bg-dark-bg border border-dark-border rounded";

    const renderContainer = (children: CanvasComponent[], parentId: string, colIndex: number, label?: string) => (
        <div
            onDragOver={onDragOver}
            onDrop={(e) => { e.preventDefault(); e.stopPropagation(); onDropInColumn(e, parentId, colIndex); }}
            className="p-4 mt-2 border-t border-dark-border min-h-[100px] space-y-4 border-2 border-dashed border-dark-border/50 rounded-lg"
        >
           {children.length > 0 ? (
                children.map(child => (
                    <ComponentRenderer key={child.id} component={child} {...{selectedComponentId, onSelectComponent, onDeleteComponent, onDropInColumn, onDragOver}} />
                ))
            ) : (
                <div className="flex items-center justify-center h-full">
                    <p className="text-dark-text-light text-sm pointer-events-none">Drop here {label && `in ${label}`}</p>
                </div>
            )}
        </div>
    );

    const renderVisualComponent = () => {
        const alignClass = {
            left: 'text-left',
            center: 'text-center',
            right: 'text-right'
        }[props.align as string] || 'text-left';

        switch (type) {
            // TEXT
            case 'title': return <h1 className={`text-4xl font-bold truncate ${alignClass}`}>{props.body as string}</h1>;
            case 'header': return <h2 className={`text-2xl font-semibold truncate ${alignClass}`}>{props.body as string}</h2>;
            case 'subheader': return <h3 className="text-xl font-medium truncate">{props.body as string}</h3>;
            case 'markdown': return <div className={`p-2 border border-dashed border-gray-600 rounded prose prose-invert prose-sm ${alignClass}`}><p className="truncate">{props.body as string}</p></div>;
            case 'caption': return <p className="text-xs text-dark-text-light truncate">{props.body as string}</p>;
            case 'code': return <pre className="bg-dark-bg p-2 rounded text-sm text-left w-full overflow-x-auto"><code>{props.body as string}</code></pre>;
            case 'latex': return <div className="p-2 border border-dashed border-gray-600 rounded text-center font-serif">ƒ: {props.body as string}</div>;
            case 'divider': return <hr className="border-dark-border" />;
            
            // DATA
            case 'table':
            case 'dataframe': return <div className="overflow-x-auto w-full border border-dark-border rounded"><table className="w-full text-sm text-left"><thead><tr className="bg-dark-border/50"><th className="p-2">col1</th><th className="p-2">col2</th></tr></thead><tbody><tr><td className="p-2">1</td><td className="p-2">10</td></tr><tr><td className="p-2">2</td><td className="p-2">20</td></tr></tbody></table></div>;
            case 'metric': return <div className="p-2 border border-dark-border rounded text-center"><div className="text-xs text-dark-text-light">{props.label as string}</div><div className="text-2xl font-bold">{props.value as string}</div><div className="text-sm text-green-400">{props.delta as string}</div></div>;
            case 'json': return <pre className="bg-dark-bg p-2 rounded text-sm text-left w-full overflow-x-auto"><code>{props.body as string}</code></pre>;
            
            // WIDGETS
            case 'button':
            case 'form_submit_button': return <button className={`bg-streamlit-red text-white font-semibold py-2 px-4 rounded truncate ${props.use_container_width ? 'w-full' : ''}`}>{props.label as string}</button>;
            case 'text_input': return <div><label className={commonInputLabelClasses}>{props.label as string}</label><input type="text" placeholder={props.placeholder as string} className={commonInputClasses} readOnly /></div>;
            case 'text_area': return <div><label className={commonInputLabelClasses}>{props.label as string}</label><textarea style={{ height: `${props.height}px` }} className={commonInputClasses} readOnly /></div>;
            case 'number_input': return <div><label className={commonInputLabelClasses}>{props.label as string}</label><input type="number" defaultValue={props.value as number} className={commonInputClasses} readOnly /></div>;
            case 'slider': return (
                <div className="w-full">
                    <label className={commonInputLabelClasses}>{props.label as string}</label>
                    <div className="flex items-center gap-2">
                        <span className="text-xs">{props.min_value}</span>
                        <input type="range" min={props.min_value as number} max={props.max_value as number} defaultValue={props.value as number} className="w-full" />
                        <span className="text-xs">{props.max_value}</span>
                    </div>
                </div>
            );
            case 'selectbox': {
                const options = (props.options as string).split(',').map(s => s.trim());
                return (
                    <div className="w-full">
                        <label className={commonInputLabelClasses}>{props.label as string}</label>
                        <select className={commonInputClasses} disabled>
                            {options.map((opt, i) => <option key={i}>{opt}</option>)}
                        </select>
                    </div>
                );
            }
             case 'multiselect': {
                return (
                    <div className="w-full">
                        <label className={commonInputLabelClasses}>{props.label as string}</label>
                        <div className={`${commonInputClasses} h-24 overflow-y-auto`}>
                            <p className="text-dark-text-light text-sm italic">Multiselect options...</p>
                        </div>
                    </div>
                );
            }
            case 'checkbox': return <div className="flex items-center gap-2"><input type="checkbox" defaultChecked={props.value as boolean} className="form-checkbox h-5 w-5 rounded bg-dark-bg border-dark-border text-streamlit-red focus:ring-streamlit-red" /><label className="text-dark-text-light">{props.label as string}</label></div>;
            case 'toggle': return <div className="flex items-center gap-2"><div className={`w-12 h-6 flex items-center rounded-full p-1 duration-300 cursor-pointer ${props.value ? 'bg-streamlit-red' : 'bg-gray-600'}`}><div className={`bg-white w-4 h-4 rounded-full shadow-md transform duration-300 ${props.value ? 'translate-x-6' : ''}`}></div></div><label className="text-dark-text-light">{props.label as string}</label></div>
            case 'radio': {
                const options = (props.options as string).split(',').map(s => s.trim());
                return (
                    <div className="w-full text-left">
                        <label className={commonInputLabelClasses}>{props.label as string}</label>
                        <div className={`flex gap-4 ${props.horizontal ? 'flex-row' : 'flex-col'}`}>
                            {options.map((opt, i) => (<div key={i} className="flex items-center"><input type="radio" name={component.id} defaultChecked={i===0} className="form-radio h-4 w-4 text-streamlit-red bg-dark-bg border-dark-border" /><span className="ml-2 text-sm">{opt}</span></div>))}
                        </div>
                    </div>
                );
            }
            case 'date_input': return <div><label className={commonInputLabelClasses}>{props.label as string}</label><input type="text" value="2024-01-01" className={commonInputClasses} readOnly /></div>
            case 'time_input': return <div><label className={commonInputLabelClasses}>{props.label as string}</label><input type="text" value="12:30" className={commonInputClasses} readOnly /></div>
            case 'file_uploader': return <div><label className={commonInputLabelClasses}>{props.label as string}</label><div className={`${commonInputClasses} text-center border-dashed`}>Browse files</div></div>
            case 'camera_input': return <div><label className={commonInputLabelClasses}>{props.label as string}</label><div className={`${commonInputClasses} text-center border-dashed`}>Take photo</div></div>
            case 'color_picker': return <div><label className={commonInputLabelClasses}>{props.label as string}</label><div className="flex items-center gap-2"><input type="color" value={props.value as string} className="w-8 h-8 p-0 border-none rounded" disabled /><span className="text-sm font-mono">{props.value as string}</span></div></div>
            
            // MEDIA
            case 'image': return <div className="text-center"><ImageIcon /><p className="text-xs mt-1 text-dark-text-light">{props.caption as string || 'Image'}</p></div>;
            case 'audio': return <div className="text-center"><AudioIcon /><p className="text-xs mt-1 text-dark-text-light">Audio Player</p></div>;
            case 'video': return <div className="text-center"><VideoIcon /><p className="text-xs mt-1 text-dark-text-light">Video Player</p></div>;

            // LAYOUT
            case 'expander': return <details className="p-2 border border-dark-border rounded w-full" open={props.expanded as boolean}><summary className="cursor-pointer font-semibold">{props.label as string}</summary>{renderContainer(component.children?.[0] || [], component.id, 0)}</details>;
            case 'container': return <div className={`w-full ${props.border ? 'p-2 border border-dark-border rounded' : ''}`}>{renderContainer(component.children?.[0] || [], component.id, 0)}</div>;
            case 'form': return <form className="p-2 border border-dashed border-dark-border rounded w-full">{renderContainer(component.children?.[0] || [], component.id, 0, `form '${props.key}'`)}</form>;
            case 'tabs': {
                const [activeTab, setActiveTab] = useState(0);
                const labels = (props.labels as string).split(',').map(s => s.trim());
                return (
                    <div className="w-full">
                        <div className="flex border-b border-dark-border">
                            {labels.map((label, index) => <button key={index} onClick={() => setActiveTab(index)} className={`py-2 px-4 text-sm font-medium ${index === activeTab ? 'border-b-2 border-streamlit-red text-streamlit-red' : 'text-dark-text-light hover:bg-dark-border/50'}`}>{label}</button>)}
                        </div>
                        {renderContainer(component.children?.[activeTab] || [], component.id, activeTab, labels[activeTab])}
                    </div>
                );
            }
            case 'columns': {
                const specString = (props.spec as string) || '1,1';
                const spec = specString.split(',').map(s => parseFloat(s.trim()) || 1);
                return (
                    <div className="flex gap-4 w-full">
                        {(component.children || []).map((columnComponents, i) => (
                            <div key={i} style={{ flexGrow: spec[i] || 1 }} className="min-w-0">
                                {renderContainer(columnComponents, component.id, i)}
                            </div>
                        ))}
                    </div>
                );
            }
            
            // STATUS
            case 'error': return <div className="p-3 rounded-md bg-red-900/50 text-red-200 border border-red-700 flex items-center"><InfoIcon />{props.body as string}</div>;
            case 'warning': return <div className="p-3 rounded-md bg-yellow-900/50 text-yellow-200 border border-yellow-700 flex items-center"><InfoIcon />{props.body as string}</div>;
            case 'info': return <div className="p-3 rounded-md bg-blue-900/50 text-blue-200 border border-blue-700 flex items-center"><InfoIcon />{props.body as string}</div>;
            case 'success': return <div className="p-3 rounded-md bg-green-900/50 text-green-200 border border-green-700 flex items-center"><InfoIcon />{props.body as string}</div>;

            default: return <div className="p-2 bg-gray-700 rounded">Unsupported component: {type}</div>;
        }
    };
    
    const isFullWidthWidget = (props.use_container_width || ['slider', 'text_input', 'selectbox', 'text_area', 'number_input'].includes(type));
    const isCentered = ['button', 'checkbox', 'toggle', 'radio', 'date_input', 'time_input', 'color_picker', 'metric'].includes(type);
    const wrapperClasses = `relative p-4 rounded-md transition-all duration-200 cursor-pointer ${selectedComponentId === component.id ? 'ring-2 ring-streamlit-red' : 'hover:bg-dark-border/50'} ${!isFullWidthWidget && isCentered ? 'flex justify-center' : ''}`;

    return (
        <div onClick={(e) => { e.stopPropagation(); onSelectComponent(component.id); }} className={wrapperClasses}>
            {renderVisualComponent()}
            {selectedComponentId === component.id && (
                <button
                    onClick={(e) => { e.stopPropagation(); onDeleteComponent(component.id); }}
                    className="absolute -top-2 -right-2 bg-red-600 hover:bg-red-700 text-white rounded-full p-1.5 z-10"
                    aria-label="Delete component"
                >
                    <TrashIcon />
                </button>
            )}
        </div>
    );
};

const Canvas: React.FC<CanvasProps> = ({ components, selectedComponentId, onDrop, onDropInColumn, onDragOver, onSelectComponent, onDeleteComponent }) => {
    return (
        <main
            className="flex-1 p-8 bg-dark-bg overflow-auto"
            style={{
                backgroundImage: 'radial-gradient(circle at 1px 1px, rgba(255,255,255,0.1) 1px, transparent 0)',
                backgroundSize: '20px 20px'
            }}
            onDrop={onDrop}
            onDragOver={onDragOver}
            onClick={() => onSelectComponent('')}
        >
            <div className="max-w-3xl mx-auto bg-dark-card shadow-lg rounded-lg p-6 min-h-full">
                {components.length === 0 ? (
                    <div className="flex items-center justify-center h-96 border-2 border-dashed border-dark-border rounded-lg">
                        <p className="text-dark-text-light">Drop components here to start building</p>
                    </div>
                ) : (
                    <div className="space-y-6">
                        {components.map(component => (
                            <ComponentRenderer
                                key={component.id}
                                component={component}
                                selectedComponentId={selectedComponentId}
                                onSelectComponent={onSelectComponent}
                                onDeleteComponent={onDeleteComponent}
                                onDropInColumn={onDropInColumn}
                                onDragOver={onDragOver}
                            />
                        ))}
                    </div>
                )}
            </div>
        </main>
    );
};

export default Canvas;