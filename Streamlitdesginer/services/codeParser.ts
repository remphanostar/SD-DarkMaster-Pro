import type { CanvasComponent } from '../types';
import { STREAMLIT_COMPONENTS } from '../constants';

// Helper to parse python literals to JS
const parsePythonLiteral = (val: string): any => {
    val = val.trim();
    if (val === 'True') return true;
    if (val === 'False') return false;

    if ((val.startsWith("'") && val.endsWith("'")) || (val.startsWith('"') && val.endsWith('"'))) {
        return val.slice(1, -1).replace(/\\'/g, "'").replace(/\\"/g, '"');
    }
    if (val.startsWith('"""') && val.endsWith('"""')) {
        return val.slice(3, -3);
    }
    
    if (!isNaN(Number(val))) return Number(val);
    
    if (val.startsWith('[') && val.endsWith(']')) {
        const content = val.slice(1, -1).trim();
        if (content === '') return [];
        // Handle lists of numbers (for columns) or strings (for tabs/selectbox)
        const items = content.split(',').map(item => item.trim());
        if (items.every(item => !isNaN(Number(item)))) {
            return items.map(Number);
        }
        const listRegex = /'([^']*)'|"([^"]*)"/g;
        let match;
        const result = [];
        while((match = listRegex.exec(content)) !== null) {
            result.push(match[1] || match[2]);
        }
        return result;
    }
    // Return as is for things like dicts, which will be stored as a string
    return val;
};

const parseProps = (propsStr: string, componentType: string): { [key: string]: any } => {
    const props: { [key: string]: any } = {};
    // Updated Regex to handle nested structures better (not perfectly, but better for dicts)
    const propsRegex = /(\w+)\s*=\s*({[\s\S]*}|\[[\s\S]*?\]|"""[\s\S]*?"""|'[^']*'|"[^"]*"|[\w\d\.]+)/g;
    let match;
    
    let tempStr = propsStr;
    if (['dataframe', 'table', 'json'].includes(componentType)) {
        // For data components, treat the whole argument as the data/body prop
        const definition = STREAMLIT_COMPONENTS[componentType];
        if (definition) {
            const firstPropName = definition.properties[0].name;
            props[firstPropName] = parsePythonLiteral(propsStr);
            return props;
        }
    }


    while ((match = propsRegex.exec(tempStr)) !== null) {
        props[match[1]] = parsePythonLiteral(match[2]);
    }
    
    const definition = STREAMLIT_COMPONENTS[componentType];
    // Handle positional arguments for simple components
    if (definition && Object.keys(props).length === 0 && propsStr.trim().length > 0 && !propsStr.includes('=')) {
        if (definition.properties.length > 0) {
            const firstPropName = definition.properties[0].name;
            props[firstPropName] = parsePythonLiteral(propsStr);
        }
    }
    return props;
};

const getIndentLevel = (line: string) => (line.match(/^\s*/) || [''])[0].length;

const getIndentedBlock = (lines: string[], startIndex: number): { blockLines: string[], linesConsumed: number } => {
    const blockLines: string[] = [];
    if (startIndex >= lines.length) return { blockLines, linesConsumed: 0 };

    const firstLine = lines[startIndex];
    if(!firstLine) return { blockLines, linesConsumed: 0 };
    
    const firstIndent = getIndentLevel(firstLine);

    for (let i = startIndex; i < lines.length; i++) {
        const line = lines[i];
        if (line.trim() === '') continue;
        const currentIndent = getIndentLevel(line);
        if (currentIndent < firstIndent) {
            return { blockLines, linesConsumed: i - startIndex };
        }
        // De-dent the line to be parsed recursively
        blockLines.push(line.substring(firstIndent));
    }
    return { blockLines, linesConsumed: lines.length - startIndex };
};


const createComponent = (type: string, props: { [key: string]: any }): CanvasComponent => {
    const definition = STREAMLIT_COMPONENTS[type];
    if (!definition) throw new Error(`Unknown component type: ${type}`);

    const finalProps: { [key: string]: any } = {};
    for (const propDef of definition.properties) {
        finalProps[propDef.name] = props[propDef.name] ?? propDef.defaultValue;
    }
    
    const newComponent: CanvasComponent = {
        id: `${type}-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`,
        type,
        props: finalProps,
    };

    if (['columns', 'expander', 'tabs', 'container', 'form'].includes(type)) {
        newComponent.children = [];
    }
    return newComponent;
};

const parseCodeRecursive = (lines: string[]): CanvasComponent[] => {
    const components: CanvasComponent[] = [];
    let i = 0;

    while (i < lines.length) {
        const line = lines[i];
        const trimmedLine = line.trim();
        if (trimmedLine === '' || trimmedLine.startsWith('#')) {
            i++;
            continue;
        }

        let match;
        
        // Match container blocks: with st.expander(...), with st.container(...), etc.
        match = trimmedLine.match(/^with st\.(expander|container|form)\((.*)\):/);
        if (match) {
            const type = match[1];
            const props = parseProps(match[2], type);
            const component = createComponent(type, props);
            const { blockLines, linesConsumed } = getIndentedBlock(lines, i + 1);
            component.children = [parseCodeRecursive(blockLines)];
            components.push(component);
            i += 1 + linesConsumed;
            continue;
        }

        // Match columns
        match = trimmedLine.match(/^([\w\s,]+)\s*=\s*st\.columns\((.*)\)/);
        if (match) {
            const specArg = match[2].trim();
            const colVars = match[1].split(',').map(s => s.trim());
            let spec: string;

            if (specArg.startsWith('[') && specArg.endsWith(']')) {
                spec = specArg.slice(1, -1).trim().replace(/\s/g, '');
            } else {
                const count = parseInt(specArg, 10) || 2;
                spec = Array(count).fill('1').join(',');
            }

            const component = createComponent('columns', { spec });
            const count = spec.split(',').length;
            component.children = Array.from({ length: count }, () => []);

            let blockEndIndex = i + 1;
            
            for (let colIndex = 0; colIndex < colVars.length; colIndex++) {
                const colVar = colVars[colIndex];
                let withStartIndex = -1;
                for (let j = i + 1; j < lines.length; j++) {
                    if (lines[j].trim() === `with ${colVar}:`) {
                        withStartIndex = j;
                        break;
                    }
                }
                if (withStartIndex > -1) {
                    const { blockLines, linesConsumed } = getIndentedBlock(lines, withStartIndex + 1);
                    if (component.children) {
                        component.children[colIndex] = parseCodeRecursive(blockLines);
                    }
                    blockEndIndex = Math.max(blockEndIndex, withStartIndex + 1 + linesConsumed);
                }
            }
            components.push(component);
            i = blockEndIndex;
            continue;
        }

        // Match tabs
        match = trimmedLine.match(/^([\w\s,]+)\s*=\s*st\.tabs\((.*)\)/);
        if (match) {
            const labelsProp = parsePythonLiteral(match[2]);
            const labels = Array.isArray(labelsProp) ? labelsProp.join(',') : '';
            const tabVars = match[1].split(',').map(s => s.trim());
            const component = createComponent('tabs', { labels });
            component.children = Array.from({ length: tabVars.length }, () => []);
            let blockEndIndex = i + 1;

            for (let tabIndex = 0; tabIndex < tabVars.length; tabIndex++) {
                const tabVar = tabVars[tabIndex];
                let withStartIndex = -1;
                for (let j = i + 1; j < lines.length; j++) {
                    if (lines[j].trim() === `with ${tabVar}:`) { withStartIndex = j; break; }
                }
                if (withStartIndex > -1) {
                    const { blockLines, linesConsumed } = getIndentedBlock(lines, withStartIndex + 1);
                     if (component.children) {
                        component.children[tabIndex] = parseCodeRecursive(blockLines);
                    }
                    blockEndIndex = Math.max(blockEndIndex, withStartIndex + 1 + linesConsumed);
                }
            }
            components.push(component);
            i = blockEndIndex;
            continue;
        }
        
        // Match button conditional blocks
        match = trimmedLine.match(/^if st\.button\((.*)\):/);
        if(match) {
            const props = parseProps(match[1], 'button');
            components.push(createComponent('button', props));
            const { linesConsumed } = getIndentedBlock(lines, i + 1);
            i += 1 + linesConsumed;
            continue;
        }

        // Match all other st.component calls
        match = trimmedLine.match(/^(?:[\w_]+\s*=\s*)?st\.(\w+)\(([\s\S]*?)\)$/);
        if (match) {
            let type = match[1];
            const propsStr = match[2].trim();
            
            // Handle `st.divider()` with no args
            if (type === 'divider' && propsStr === '') {
                 components.push(createComponent('divider', {}));
                 i++;
                 continue;
            }
            
            let props = parseProps(propsStr, type);

            // Handle aligned text from markdown
            if (type === 'markdown' && props.unsafe_allow_html) {
                 const content = props.body as string || '';
                 const h1Match = content.match(/<h1 style='text-align: (center|right);'>(.*?)<\/h1>/);
                 if (h1Match) { type = 'title'; props = { body: h1Match[2].replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#039;/g, "'"), align: h1Match[1] }; }
                 const h2Match = content.match(/<h2 style='text-align: (center|right);'>(.*?)<\/h2>/);
                 if (h2Match) { type = 'header'; props = { body: h2Match[2].replace(/&amp;/g, "&").replace(/&lt;/g, "<").replace(/&gt;/g, ">").replace(/&quot;/g, '"').replace(/&#039;/g, "'"), align: h2Match[1] }; }
                 const divMatch = content.match(/<div style='text-align: (center|right);'>\n([\s\S]*)\n<\/div>/);
                 if (divMatch) { type = 'markdown'; props = { body: divMatch[2], align: divMatch[1] }; }
            }
            
            if (['selectbox', 'multiselect', 'radio'].includes(type) && props.options && Array.isArray(props.options)) {
                props.options = props.options.join(',');
            }
            
            if(type === 'dataframe' || type === 'table') {
                 props.data = propsStr.replace(/^pd\.DataFrame\((.*)\)$/, '$1');
            }
            
            if (STREAMLIT_COMPONENTS[type]) {
                components.push(createComponent(type, props));
            }

            i++;
            continue;
        }
        
        i++;
    }
    return components;
};

export const parseStreamlitCode = (code: string): CanvasComponent[] => {
    const lines = code.split('\n').filter(line => 
        !line.trim().startsWith('import ') && 
        !line.trim().startsWith('st.write(f\'The current value') &&
        !line.trim().startsWith('pass')
    );
    return parseCodeRecursive(lines);
};