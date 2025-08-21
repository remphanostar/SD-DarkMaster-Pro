import React from 'react';
import type { StreamlitComponentDefinition } from './types';
import { PropertyType } from './types';

// Icons are now h-5 w-5 for a more compact sidebar
const TitleIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v2h16V4m-8 16V6M7 14h10" /></svg>;
const TextIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h7" /></svg>;
const ButtonIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 15l-2 5L9 9l11 4-5 2zm0 0l5 5M7.188 8.812a9.025 9.025 0 0112.728 0M11 11a1 1 0 11-2 0 1 1 0 012 0z" /></svg>;
const TextInputIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 4H4a2 2 0 00-2 2v14a2 2 0 002 2h14a2 2 0 002 2v-7" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.5 2.5a2.121 2.121 0 013 3L12 15l-4 1 1-4 9.5-9.5z" /></svg>;
const SliderIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M18.364 18.364A9 9 0 005.636 5.636m12.728 12.728A9 9 0 015.636 5.636m12.728 12.728L18 18m-1.636-1.636l-1.414-1.414" /></svg>;
const CheckboxIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>;
const SelectboxIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 9l4-4 4 4m0 6l-4 4-4-4" /></svg>;
const ExpanderIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" /></svg>;
const TabsIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 7v10a2 2 0 002 2h12a2 2 0 002-2V7M6 5h12M9 3h6" /></svg>;
const ColumnsIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 4v16m-6-16h12a2 2 0 012 2v12a2 2 0 01-2 2H6a2 2 0 01-2-2V6a2 2 0 012-2z" /></svg>;
const SubheaderIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 10h16M4 14h10" /></svg>;
const CaptionIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16h12M4 20h6" /></svg>;
const CodeIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" /></svg>;
const LatexIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><text x="4" y="20" fontSize="18" fill="currentColor">Σ</text></svg>;
const DividerIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 12h16" /></svg>;
const TextAreaIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 6h18M3 10h18M3 14h18M3 18h18" /></svg>;
const NumberInputIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 20v-4M10 20v-8M13 20V4M16 20v-4" /><path d="M4 4h16v4H4z" /></svg>;
const DateInputIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>;
const TimeInputIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>;
const ColorPickerIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" /></svg>;
const RadioIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 7v3m0 4v3m-4-7h8m-4 7a5 5 0 100-10 5 5 0 000 10z" /></svg>;
const MultiselectIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m-6 5h10M5 7h14" /></svg>;
const ToggleIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 15s1-1 4-1 5 2 8 2 4-1 4-1V3s-1 1-4 1-5-2-8-2-4 1-4 1v12z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 9h16" /></svg>;
const FileUploaderIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" /></svg>;
const CameraInputIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 2 0 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0018.07 7H19a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" /><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" /></svg>;
const ImageIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" /></svg>;
const AudioIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15.536 8.464a5 5 0 010 7.072m2.828-9.9a9 9 0 010 12.728M5.858 5.858a3 3 0 104.243 4.243L5.858 14.343a3 3 0 00-4.243-4.243l4.243-4.243z" /></svg>;
const VideoIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z" /></svg>;
const MetricIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" /></svg>;
const DataframeIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 10h18M3 14h18M3 6h18M9 20h6" /></svg>;
const JsonIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 9l-3 3 3 3m8-6l3 3-3 3M10 21v-2a4 4 0 00-4-4H4" /><path d="M14 3v2a4 4 0 004 4h2" /></svg>;
const StatusIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>;
const ContainerIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20 12H4" /><path d="M20 7H4v10h16V7z" /></svg>;
const FormIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg>;

export const COMPONENT_CATEGORIES = [
    {
        name: 'Text',
        components: {
            title: {
                name: 'Title',
                icon: <TitleIcon />,
                isWidget: false,
                properties: [
                    { name: 'body', label: 'Title Text', type: PropertyType.STRING, defaultValue: 'My Awesome App' },
                    { name: 'align', label: 'Alignment', type: PropertyType.STRING, defaultValue: 'left', options: ['left', 'center', 'right'] },
                ],
            },
            header: {
                name: 'Header',
                icon: <TitleIcon />,
                isWidget: false,
                properties: [
                    { name: 'body', label: 'Header Text', type: PropertyType.STRING, defaultValue: 'This is a header' },
                    { name: 'align', label: 'Alignment', type: PropertyType.STRING, defaultValue: 'left', options: ['left', 'center', 'right'] },
                ],
            },
            subheader: {
                name: 'Subheader',
                icon: <SubheaderIcon />,
                isWidget: false,
                properties: [
                    { name: 'body', label: 'Subheader Text', type: PropertyType.STRING, defaultValue: 'This is a subheader' },
                ],
            },
            markdown: {
                name: 'Markdown',
                icon: <TextIcon />,
                isWidget: false,
                properties: [
                    { name: 'body', label: 'Markdown Content', type: PropertyType.MARKDOWN, defaultValue: 'Hello, **Streamlit**! You can use `markdown`.' },
                    { name: 'align', label: 'Alignment', type: PropertyType.STRING, defaultValue: 'left', options: ['left', 'center', 'right'] },
                ],
            },
            caption: {
                name: 'Caption',
                icon: <CaptionIcon />,
                isWidget: false,
                properties: [
                    { name: 'body', label: 'Caption Text', type: PropertyType.STRING, defaultValue: 'This is a caption.' },
                ],
            },
            code: {
                name: 'Code',
                icon: <CodeIcon />,
                isWidget: false,
                properties: [
                    { name: 'body', label: 'Code Content', type: PropertyType.MARKDOWN, defaultValue: 'def hello():\n    print("Hello, Streamlit!")' },
                    { name: 'language', label: 'Language', type: PropertyType.STRING, defaultValue: 'python' },
                ],
            },
            latex: {
                name: 'LaTeX',
                icon: <LatexIcon />,
                isWidget: false,
                properties: [
                    { name: 'body', label: 'LaTeX Expression', type: PropertyType.STRING, defaultValue: 'e^{i\pi} + 1 = 0' },
                ],
            },
            divider: {
                name: 'Divider',
                icon: <DividerIcon />,
                isWidget: false,
                properties: [],
            },
        }
    },
    {
        name: 'Data',
        components: {
            dataframe: {
                name: 'Dataframe',
                icon: <DataframeIcon />,
                isWidget: false,
                properties: [
                    { name: 'data', label: 'Data (Python Dict)', type: PropertyType.MARKDOWN, defaultValue: '{\n    "col1": [1, 2, 3],\n    "col2": [10, 20, 30]\n}' },
                ],
            },
            table: {
                name: 'Table',
                icon: <DataframeIcon />,
                isWidget: false,
                properties: [
                    { name: 'data', label: 'Data (Python Dict)', type: PropertyType.MARKDOWN, defaultValue: '{\n    "col1": [1, 2, 3],\n    "col2": [10, 20, 30]\n}' },
                ],
            },
            metric: {
                name: 'Metric',
                icon: <MetricIcon />,
                isWidget: false,
                properties: [
                    { name: 'label', label: 'Label', type: PropertyType.STRING, defaultValue: 'Temperature' },
                    { name: 'value', label: 'Value', type: PropertyType.STRING, defaultValue: '70 °F' },
                    { name: 'delta', label: 'Delta', type: PropertyType.STRING, defaultValue: '1.2 °F' },
                ],
            },
            json: {
                name: 'JSON',
                icon: <JsonIcon />,
                isWidget: false,
                properties: [
                    { name: 'body', label: 'JSON Object (string)', type: PropertyType.MARKDOWN, defaultValue: '{\n    "foo": "bar",\n    "baz": "qux"\n}' },
                ],
            },
        }
    },
    {
        name: 'Inputs',
        components: {
            button: {
                name: 'Button',
                icon: <ButtonIcon />,
                isWidget: true,
                properties: [
                    { name: 'label', label: 'Button Label', type: PropertyType.STRING, defaultValue: 'Click me' },
                    { name: 'use_container_width', label: 'Full Width', type: PropertyType.BOOLEAN, defaultValue: false },
                ],
            },
            form_submit_button: {
                name: 'Submit Button',
                icon: <ButtonIcon />,
                isWidget: true,
                properties: [
                    { name: 'label', label: 'Button Label', type: PropertyType.STRING, defaultValue: 'Submit' },
                    { name: 'use_container_width', label: 'Full Width', type: PropertyType.BOOLEAN, defaultValue: false },
                ],
            },
            text_input: {
                name: 'Text Input',
                icon: <TextInputIcon />,
                isWidget: true,
                properties: [
                    { name: 'label', label: 'Label', type: PropertyType.STRING, defaultValue: 'Enter some text' },
                    { name: 'placeholder', label: 'Placeholder', type: PropertyType.STRING, defaultValue: 'Type here...' },
                ],
            },
            text_area: {
                name: 'Text Area',
                icon: <TextAreaIcon />,
                isWidget: true,
                properties: [
                    { name: 'label', label: 'Label', type: PropertyType.STRING, defaultValue: 'Enter a longer text' },
                    { name: 'height', label: 'Height (px)', type: PropertyType.NUMBER, defaultValue: 150 },
                ],
            },
            number_input: {
                name: 'Number Input',
                icon: <NumberInputIcon />,
                isWidget: true,
                properties: [
                    { name: 'label', label: 'Label', type: PropertyType.STRING, defaultValue: 'Enter a number' },
                    { name: 'min_value', label: 'Min Value', type: PropertyType.NUMBER, defaultValue: 0 },
                    { name: 'max_value', label: 'Max Value', type: PropertyType.NUMBER, defaultValue: 100 },
                    { name: 'value', label: 'Default Value', type: PropertyType.NUMBER, defaultValue: 25 },
                ],
            },
            slider: {
                name: 'Slider',
                icon: <SliderIcon />,
                isWidget: true,
                properties: [
                    { name: 'label', label: 'Label', type: PropertyType.STRING, defaultValue: 'Select a range' },
                    { name: 'min_value', label: 'Min Value', type: PropertyType.NUMBER, defaultValue: 0 },
                    { name: 'max_value', label: 'Max Value', type: PropertyType.NUMBER, defaultValue: 100 },
                    { name: 'value', label: 'Default Value', type: PropertyType.NUMBER, defaultValue: 50 },
                ],
            },
            selectbox: {
                name: 'Selectbox',
                icon: <SelectboxIcon />,
                isWidget: true,
                properties: [
                    { name: 'label', label: 'Label', type: PropertyType.STRING, defaultValue: 'Choose an option' },
                    { name: 'options', label: 'Options (comma-separated)', type: PropertyType.STRING, defaultValue: 'Option 1,Option 2,Option 3' },
                ],
            },
            multiselect: {
                name: 'Multiselect',
                icon: <MultiselectIcon />,
                isWidget: true,
                properties: [
                    { name: 'label', label: 'Label', type: PropertyType.STRING, defaultValue: 'Choose options' },
                    { name: 'options', label: 'Options (comma-separated)', type: PropertyType.STRING, defaultValue: 'Option 1,Option 2,Option 3' },
                ],
            },
            checkbox: {
                name: 'Checkbox',
                icon: <CheckboxIcon />,
                isWidget: true,
                properties: [
                    { name: 'label', label: 'Label', type: PropertyType.STRING, defaultValue: 'I agree to the terms' },
                    { name: 'value', label: 'Checked by default', type: PropertyType.BOOLEAN, defaultValue: false },
                ],
            },
            toggle: {
                name: 'Toggle',
                icon: <ToggleIcon />,
                isWidget: true,
                properties: [
                    { name: 'label', label: 'Label', type: PropertyType.STRING, defaultValue: 'Enable feature' },
                    { name: 'value', label: 'On by default', type: PropertyType.BOOLEAN, defaultValue: false },
                    { name: 'display_as', label: 'Display As', type: PropertyType.STRING, defaultValue: 'switch', options: ['switch', 'button'] },
                ],
            },
            radio: {
                name: 'Radio',
                icon: <RadioIcon />,
                isWidget: true,
                properties: [
                    { name: 'label', label: 'Label', type: PropertyType.STRING, defaultValue: 'Select one' },
                    { name: 'options', label: 'Options (comma-separated)', type: PropertyType.STRING, defaultValue: 'Opt A,Opt B,Opt C' },
                    { name: 'horizontal', label: