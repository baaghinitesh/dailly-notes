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

const files = walk('d:/projects/dailly-notes/docs/notes');
let filesNeedingFix = [];

files.forEach(file => {
    try {
        let content = fs.readFileSync(file, 'utf8');
        let newContent = content;
        
        const mermaidRegex = /```mermaid\s+([\s\S]*?)```/g;
        
        newContent = newContent.replace(mermaidRegex, (match, block) => {
            let newBlock = block;
            
            // We need to find node definitions:
            // Node shapes in mermaid:
            // id1[Text]
            // id1(Text)
            // id1([Text])
            // id1[[Text]]
            // id1[(Text)]
            // id1((Text))
            // id1>Text]
            // id1{Text}
            // id1{{Text}}
            // id1[/Text/]
            // id1[\Text\]
            // id1[/Text\]
            // id1[\Text/]
            // The safest way is to find a typical text definition which is NodeIdentifier plus some brackets.
            // Let's look for NodeID[Text], NodeID{Text}, NodeID(Text)
            // where Text contains (, ), [, ], /, ?, etc., AND is not already quoted.
            
            // Regex for NodeID[Text] where Text is not starting with "
            // The [^\]]+ means any character except ]
            newBlock = newBlock.replace(/([A-Za-z0-9_-]+)\[([^"\]][^\]]*)\]/g, (m, id, text) => {
                if (text.match(/[\(\)\{\}\[\]\?\/\>]/)) {
                    return `${id}["${text}"]`;
                }
                return m;
            });

            // Regex for NodeID{Text}
            newBlock = newBlock.replace(/([A-Za-z0-9_-]+)\{([^"\}][^\}]*)\}/g, (m, id, text) => {
                if (text.match(/[\(\)\{\}\[\]\?\/\>]/)) {
                    return `${id}{"${text}"}`;
                }
                return m;
            });

            // Regex for NodeID(Text) (Wait, this might match subgraph or other syntax, but within limits of typical node definitions, it's ok)
            // Actually, (Text) can conflict with other markdown. So only apply to obvious nodes
            newBlock = newBlock.replace(/([A-Za-z0-9_-]+)\(([^"\)][^\)]*)\)/g, (m, id, text) => {
                // Ignore if it's a known keyword or shape definition without chars
                if (text.match(/[\(\)\{\}\[\]\?\/\>]/)) {
                    return `${id}("${text}")`;
                }
                return m;
            });

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

console.log(`Replaced unquoted special chars in ${filesNeedingFix.length} files.`);
console.log(filesNeedingFix);
