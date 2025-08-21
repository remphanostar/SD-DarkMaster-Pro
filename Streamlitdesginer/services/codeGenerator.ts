import type { CanvasComponent } from '../types';
import { STREAMLIT_COMPONENTS } from '../constants';

const formatValue = (value: any): string => {
    if (typeof value === 'string') {
        // Use triple quotes for multiline strings that are not valid python dicts/lists
        if (value.includes('\n') && !/^\s*\{|\[/.test(value)) {
            return `"""${value.replace(/"/g, '\\"')}"""`;
        }
        return `'${value.replace(/'/g, "\\'")}'`;
    }
    if (typeof value === 'boolean') {
        return value ? 'True' : 'False';
    }
    // For raw data like python dicts
    if (String(value).trim().startsWith('{') || String(value).trim().startsWith('[')) {
        return String(value);
    }
    return String(value);
};

const escapeForHtml = (str: string): string => {
    return str
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
};


const generateCodeRecursive = (components: CanvasComponent[], context: { widgetCount: number, usesPandas: boolean }, indent: string): string => {
    return components.map(component => {
        const definition = STREAMLIT_COMPONENTS[component.type];
        if (!definition) return '';
        const currentIndent = indent;

        const align = component.props.align as string;
        if (['title', 'header', 'markdown'].includes(component.type) && align && align !== 'left') {
            const body = component.props.body as string;
            let content = '';
            if (component.type === 'title') {
                content = `<h1 style='text-align: ${align};'>${escapeForHtml(body)}</h1>`;
            } else if (component.type === 'header') {
                content = `<h2 style='text-align: ${align};'>${escapeForHtml(body)}</h2>`;
            } else { // markdown
                content = `<div style='text-align: ${align};'>\n${body}\n</div>`;
            }
            return `${currentIndent}st.markdown(${formatValue(content)}, unsafe_allow_html=True)`;
        }

        const propsString = Object.entries(component.props)
            .map(([key, value]) => {
                if (
                    (component.type === 'tabs' && key === 'labels') ||
                    (component.type === 'columns' && key === 'spec') ||
                    (component.type === 'image' && key === 'src') ||
                    (component.type === 'audio' && key === 'src') ||
                    (component.type === 'video' && key === 'src') ||
                    (component.type === 'form' && key === 'key') ||
                    key === 'align'
                ) {
                    return null;
                }
                
                if (key === 'use_container_width' && value === false) return null;
                if (key === 'expanded' && value === false) return null;
                if (key === 'border' && value === false) return null;
                if (key === 'clear_on_submit' && value === false) return null;
                if (key === 'horizontal' && value === false) return null;
                if (component.type === 'image' && key === 'width' && Number(value) === 0) return null;
                if (component.type === 'file_uploader' && key === 'type' && value === '') return null;


                if ((component.type === 'selectbox' || component.type === 'multiselect' || component.type === 'radio') && key === 'options') {
                    const options = String(value).split(',').map(s => s.trim());
                    const optionsListString = `[${options.map(formatValue).join(', ')}]`;
                    return `options=${optionsListString}`;
                }
                
                return `${key}=${formatValue(value)}`;
            })
            .filter(Boolean)
            .join(', ');

        let code = '';
        
        if (component.type === 'columns') {
            const spec = (component.props.spec as string) || '1,1';
            const specArray = spec.split(',').map(s => s.trim()).filter(Boolean);
            const count = specArray.length;
            const colVars = Array.from({ length: count }, (_, i) => `col${context.widgetCount + i + 1}`);
            context.widgetCount += count;
            code += `${currentIndent}${colVars.join(', ')} = st.columns([${spec}])\n\n`;

            component.children?.forEach((columnComponents, i) => {
                if (i < count && columnComponents.length > 0) {
                    code += `${currentIndent}with ${colVars[i]}:\n`;
                    code += generateCodeRecursive(columnComponents, context, `${currentIndent}    `);
                    code += '\n';
                }
            });
            return code.trimEnd();
        }

        if (component.type === 'expander' || component.type === 'container' || component.type === 'form') {
            let containerCode = '';
            if (component.type === 'form') {
                 containerCode = `${currentIndent}with st.form(key=${formatValue(component.props.key)}, clear_on_submit=${formatValue(component.props.clear_on_submit)}):\n`;
            } else {
                containerCode = `${currentIndent}with st.${component.type}(${propsString}):\n`;
            }
            const children = component.children?.[0] || [];
            if (children.length > 0) {
                containerCode += generateCodeRecursive(children, context, `${currentIndent}    `);
            } else {
                containerCode += `${currentIndent}    pass # Drop components here`;
            }
            return containerCode;
        }

        if (component.type === 'tabs') {
            const labels = (component.props.labels as string || 'Tab 1').split(',').map(s => s.trim());
            const tabVars = labels.map((_, i) => `tab${context.widgetCount + i + 1}`);
            context.widgetCount += labels.length;
            const tabList = JSON.stringify(labels);
            
            let tabsCode = `${currentIndent}${tabVars.join(', ')} = st.tabs(${tabList})\n\n`;
            tabsCode += tabVars.map((tabVar, i) => {
                let tabContent = `${currentIndent}with ${tabVar}:\n`;
                const children = component.children?.[i] || [];
                 if (children.length > 0) {
                    tabContent += generateCodeRecursive(children, context, `${currentIndent}    `);
                } else {
                    tabContent += `${currentIndent}    pass # Drop components here`;
                }
                return tabContent;
            }).join('\n\n');
            return tabsCode;
        }
        
        if (component.type === 'dataframe' || component.type === 'table') {
            context.usesPandas = true;
            return `${currentIndent}st.${component.type}(pd.DataFrame(${component.props.data}))`;
        }

        if (component.type === 'image' || component.type === 'audio' || component.type === 'video') {
             return `${currentIndent}st.${component.type}('${component.props.src}', ${propsString})`;
        }
        
        if (component.type === 'divider') {
            return `${currentIndent}st.divider()`;
        }
        
        if (component.type === 'form_submit_button') {
            return `${currentIndent}st.form_submit_button(${propsString})`
        }

        if (definition.isWidget) {
            context.widgetCount++;
            const varName = `${component.type}_${context.widgetCount}`;
            
            if (component.type === 'button') {
                return `${currentIndent}if st.button(${propsString}, key='${component.id}'):\n${currentIndent}    st.write(f"'${component.props.label}' button was clicked!")`;
            }

            return `${currentIndent}${varName} = st.${component.type}(${propsString}, key='${component.id}')`;
        } else {
            return `${currentIndent}st.${component.type}(${propsString})`;
        }
    }).join('\n\n');
};

export const generateStreamlitCode = (components: CanvasComponent[]): string => {
    let header = `import streamlit as st\n`;
    const context = { widgetCount: 0, usesPandas: false };
    const body = generateCodeRecursive(components, context, '');

    if (context.usesPandas) {
        header += `import pandas as pd\n`;
    }

    return header + '\n' + body;
};