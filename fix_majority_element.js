const fs = require('fs');
const file = 'd:/projects/dailly-notes/docs/notes/dsa/java/easy/Majority_Element.md';
let txt = fs.readFileSync(file, 'utf8');

txt = txt.replace('C --> D{"Is current element same as candidate?"}', 'C -->|Yes| D{"Is current element same as candidate?"}');
txt = txt.replace('B --> C[Iterate through array]', 'B --> C{"More elements in array?"}');
txt = txt.replace('C --> I[End of array]', 'C -->|No| I[End of array iteration]');
txt = txt.replace('G -->|No| C', 'G -->|No| C\n    H --> C\n    E --> C');

fs.writeFileSync(file, txt);
console.log('Fixed Majority_Element.md loop flow');
