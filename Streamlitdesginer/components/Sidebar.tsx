import React from 'react';
import { COMPONENT_CATEGORIES } from '../constants';

interface SidebarProps {
    onDragStart: (e: React.DragEvent<HTMLDivElement>, componentType: string) => void;
}

const Sidebar: React.FC<SidebarProps> = ({ onDragStart }) => {
    return (
        <aside className="w-64 bg-dark-card border-r border-dark-border p-4 flex flex-col">
            <h2 className="text-xl font-bold mb-4 text-streamlit-red flex-shrink-0">Components</h2>
            <div className="flex-grow overflow-y-auto pr-2 -mr-2 space-y-4">
                {COMPONENT_CATEGORIES.map(category => (
                    <div key={category.name}>
                        <h3 className="text-sm font-semibold text-dark-text-light mb-2">{category.name}</h3>
                        <div className="grid grid-cols-2 gap-2">
                            {Object.entries(category.components).map(([type, { name, icon }]) => (
                                <div
                                    key={type}
                                    draggable
                                    onDragStart={(e) => onDragStart(e, type)}
                                    className="flex flex-col items-center justify-center p-2 bg-dark-bg border border-dark-border rounded-lg cursor-grab hover:bg-dark-border hover:border-streamlit-red transition-all duration-200"
                                >
                                    <span className="text-streamlit-red">{icon}</span>
                                    <span className="text-xs mt-1.5 text-center text-dark-text-light">{name}</span>
                                </div>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </aside>
    );
};

export default Sidebar;
