const { spawnSync } = require('child_process');
const { generateSeed } = require('./randomize.js');

const args = process.argv.slice(2);

function invalidArgs() {
    console.log('USAGE: node start.js -i <original rom location> -o <output path for randomized rom>');
    process.exit(1);
}

if (!args || args.length !== 4) {
    invalidArgs();
}

let input, output;

for (let i = 0; i < args.length; i++) {
    if (args[i] === '-i') {
        input = args[i+1];
        i++;
    } else if (args[i] === '-o') {
        output = args[i+1];
        i++;
    } else {
        invalidArgs();
    }
}

const randomized_json = generateSeed();
console.log('Generating randomized ROM...');
const python = spawnSync('python', ['./rom_functions.py', '--output', output, '--rom', input], { encoding : 'utf8', input: JSON.stringify(randomized_json) });
console.log(python.stdout.toString())
console.log(`Done. ROM saved to ${output}`);