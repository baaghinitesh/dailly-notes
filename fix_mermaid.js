const fs = require('fs');
const path = require('path');

function walk(dir) {
    let results = [];
    const list = fs.readdirSync(dir);
    list.forEach(file => {
        file = path.join(dir, file);
        const stat = fs.statSync(file);
        if (stat && stat.isDirectory()) {
            if (!file.includes('node_modules') && !file.includes('.git')) {
                results = results.concat(walk(file));
            }
        } else if (file.endsWith('.md')) {
            results.push(file);
        }
    });
    return results;
}

const files = walk('d:/projects/dailly-notes/docs');
let filesNeedingFix = [];

files.forEach(file => {
    try {
        let content = fs.readFileSync(file, 'utf8');
        let newContent = content;
        
        // Match ```mermaid followed by whitespace (like \r\n or \n) until the closing ```
        const mermaidRegex = /```mermaid\s+([\s\S]*?)```/g;
        
        newContent = newContent.replace(mermaidRegex, (match, block) => {
            let newBlock = block;
            
            // Fix 1: Bad Edge Label Syntax: -->|Text|> Node
            // Could be -->|text|>, -.->|text|>, etc.
            newBlock = newBlock.replace(/(-+>|=+>|-+\.-+>)\|([^|]+)\|\s*>/g, '$1|$2|');
            
            // Fix 2: LR vs TD
            // The prompt says: "Use graph TD... default... 5 or more steps... "
            // "Use graph LR... ONLY for short flows ... max 3 to 4 nodes across."
            if (newBlock.match(/(graph|flowchart)\s+LR/)) {
                // Count edges as a proxy for number of steps/nodes
                const edgeCount = (newBlock.match(/-->|-.->|==>/g) || []).length;
                if (edgeCount >= 4) {
                    newBlock = newBlock.replace(/(graph|flowchart)\s+LR/, '$1 TD');
                }
            }
            
            // Fix 3: Clean up non-breaking spaces
            newBlock = newBlock.replace(/\u00A0|\u200B/g, ' ');
            
            return '```mermaid\n' + newBlock + '```';
        });

        if (newContent !== content) {
            fs.writeFileSync(file, newContent, 'utf8');
            filesNeedingFix.push(file);
        }
    } catch (err) {
        console.error("Error reading file:", file, err.message);
    }
});

console.log(`Replaced issues in ${filesNeedingFix.length} files.`);
