import React, { useState, useEffect, useCallback } from 'react';
import type { CanvasComponent } from '../types';
import { generateStreamlitCode } from '../services/codeGenerator';

interface CodeOutputProps {
    components: CanvasComponent[];
    onUpdateCanvas: (code: string) => void;
}

const ClipboardIcon = ({ copied }: { copied: boolean }) => (
    <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        {copied ? (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
        ) : (
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
        )}
    </svg>
);

const SyncIcon = () => <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h5M20 20v-5h-5M4 4l1.5 1.5A9 9 0 0120.5 10M20 20l-1.5-1.5A9 9 0 003.5 14" /></svg>;


const CodeOutput: React.FC<CodeOutputProps> = ({ components, onUpdateCanvas }) => {
    const [editableCode, setEditableCode] = useState('');
    const [copied, setCopied] = useState(false);

    useEffect(() => {
        const newCode = generateStreamlitCode(components);
        setEditableCode(newCode);
    }, [components]);

    const handleCopy = useCallback(() => {
        navigator.clipboard.writeText(editableCode).then(() => {
            setCopied(true);
            setTimeout(() => setCopied(false), 2000);
        });
    }, [editableCode]);
    
    const handleSync = () => {
        onUpdateCanvas(editableCode);
    };

    return (
        <div className="p-4 h-full flex flex-col">
            <h3 className="text-lg font-bold mb-2 border-b border-dark-border pb-2">Generated Code</h3>
            <div className="relative flex-grow">
                 <div className="absolute top-2 right-2 flex gap-2 z-10">
                    <button
                        onClick={handleSync}
                        className="p-2 bg-dark-bg border border-dark-border rounded-md hover:bg-dark-border text-dark-text-light hover:text-white transition-colors"
                        aria-label="Sync code to canvas"
                    >
                       <SyncIcon />
                    </button>
                    <button
                        onClick={handleCopy}
                        className="p-2 bg-dark-bg border border-dark-border rounded-md hover:bg-dark-border text-dark-text-light hover:text-white transition-colors"
                        aria-label="Copy code"
                    >
                        <ClipboardIcon copied={copied} />
                    </button>
                </div>
                <textarea
                    value={editableCode}
                    onChange={(e) => setEditableCode(e.target.value)}
                    spellCheck="false"
                    className="bg-dark-bg p-4 rounded-md overflow-auto h-full w-full font-mono text-sm whitespace-pre-wrap leading-relaxed resize-none focus:outline-none focus:ring-1 focus:ring-streamlit-red"
                    aria-label="Editable Python code"
                />
            </div>
        </div>
    );
};

export default CodeOutput;
