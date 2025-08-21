import React from 'react';
import type { CanvasComponent, ComponentProperty } from '../types';
import { PropertyType } from '../types';
import { STREAMLIT_COMPONENTS } from '../constants';

interface PropertiesPanelProps {
    selectedComponent: CanvasComponent | null;
    onUpdateComponent: (id: string, newProps: { [key: string]: any }) => void;
}

const PropertyInput: React.FC<{
    propDef: ComponentProperty,
    value: any,
    onChange: (name: string, value: any) => void
}> = ({ propDef, value, onChange }) => {
    const commonClasses = "w-full p-2 bg-dark-bg border border-dark-border rounded-md mt-1 focus:ring-1 focus:ring-streamlit-red focus:outline-none";

    if (propDef.options) {
        return (
            <select
                value={value}
                onChange={(e) => onChange(propDef.name, e.target.value)}
                className={commonClasses}
            >
                {propDef.options.map(option => (
                    <option key={String(option)} value={option}>{String(option)}</option>
                ))}
            </select>
        );
    }

    switch (propDef.type) {
        case PropertyType.STRING:
            return <input type="text" value={value} onChange={(e) => onChange(propDef.name, e.target.value)} className={commonClasses} />;
        case PropertyType.MARKDOWN:
            return <textarea value={value} onChange={(e) => onChange(propDef.name, e.target.value)} className={`${commonClasses} h-32 font-mono text-sm`} />;
        case PropertyType.NUMBER:
            return <input type="number" value={value} onChange={(e) => onChange(propDef.name, parseFloat(e.target.value) || 0)} className={commonClasses} />;
        case PropertyType.BOOLEAN:
            return (
                <label className="flex items-center mt-2 cursor-pointer">
                    <input
                        type="checkbox"
                        checked={value}
                        onChange={(e) => onChange(propDef.name, e.target.checked)}
                        className="form-checkbox h-5 w-5 rounded bg-dark-bg border-dark-border text-streamlit-red focus:ring-streamlit-red"
                    />
                    <span className="ml-2 text-dark-text-light">{value ? 'True' : 'False'}</span>
                </label>
            );
        case PropertyType.COLOR:
            return (
                 <div className="flex items-center gap-2 mt-1">
                    <input
                        type="color"
                        value={value}
                        onChange={(e) => onChange(propDef.name, e.target.value)}
                        className="p-0 h-10 w-10 bg-dark-bg border-dark-border rounded-md cursor-pointer"
                    />
                    <input
                        type="text"
                        value={value}
                        onChange={(e) => onChange(propDef.name, e.target.value)}
                        className={`${commonClasses} mt-0`}
                    />
                </div>
            );
        default:
            return null;
    }
};

const PropertiesPanel: React.FC<PropertiesPanelProps> = ({ selectedComponent, onUpdateComponent }) => {
    if (!selectedComponent) {
        return (
            <div className="p-4 text-center text-dark-text-light">
                <p>Select a component to edit its properties.</p>
            </div>
        );
    }

    const componentDef = STREAMLIT_COMPONENTS[selectedComponent.type];
     if (!componentDef) {
        return (
            <div className="p-4 text-center text-dark-text-light">
                <p>Unknown component selected.</p>
            </div>
        );
    }

    const handlePropChange = (name: string, value: any) => {
        onUpdateComponent(selectedComponent.id, { ...selectedComponent.props, [name]: value });
    };

    return (
        <div className="p-4">
            <h3 className="text-lg font-bold mb-4 border-b border-dark-border pb-2">Properties: <span className="text-streamlit-red">{componentDef.name}</span></h3>
            <div className="space-y-4">
                {componentDef.properties.map(propDef => (
                    <div key={propDef.name}>
                        <label className="font-semibold text-sm text-dark-text-light">{propDef.label}</label>
                        <PropertyInput
                            propDef={propDef}
                            value={selectedComponent.props[propDef.name]}
                            onChange={handlePropChange}
                        />
                    </div>
                ))}
            </div>
        </div>
    );
};

export default PropertiesPanel;