import type { ReactNode } from 'react';

export enum PropertyType {
    STRING = 'string',
    NUMBER = 'number',
    BOOLEAN = 'boolean',
    MARKDOWN = 'markdown',
    COLOR = 'color',
}

export interface ComponentProperty {
    name: string;
    label: string;
    type: PropertyType;
    defaultValue: string | number | boolean;
    options?: (string | number)[]; // For select-like inputs
}

export interface StreamlitComponentDefinition {
    name: string;
    icon: ReactNode;
    properties: ComponentProperty[];
    isWidget: boolean;
}

export interface CanvasComponent {
    id: string;
    type: string;
    props: { [key: string]: string | number | boolean };
    children?: CanvasComponent[][]; // Array of columns, each column is an array of components
}