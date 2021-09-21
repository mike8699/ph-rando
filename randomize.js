const chest_contents_list = [10, 10, 10, 10, 10, 10, 10, 25, 1, 1, 25, 12, 25, 15, 125, 35, 129, 119, 34, 118, 19, 0, 47, 125, 46, 125, 6, 6, 6, 45, 125, 20, 45, 125, 117, 98, 84, 125, 126, 34, 45, 126, 47, 35, 46, 126, 21, 9, 105, 117, 26, 125, 6, 6, 27, 106, 126, 22, 135, 135, 125, 126, 45, 1, 8, 46, 9, 33, 15, 45, 125, 47, 25, 97, 14, 134, 15, 134, 25, 45, 46, 117, 119, 1, 46, 32, 15, 1, 118, 15, 47, 125, 7, 45, 125, 31, 15, 9, 1, 1, 47, 25, 47, 9, 47, 45, 113, 46, 126, 9, 125, 126, 45, 47, 3, 60, 103, 47, 99, 133, 133, 45, 47, 125, 38, 45, 46, 79, 125, 13, 9, 45, 77, 47, 45, 47, 46, 102, 10, 27, 46, 47, 27, 47, 82, 25, 121, 122, 123, 124, 46, 45, 25, 25, 9, 45, 78, 47, 46, 86, 46, 45, 46, 47, 26, 9, 46, 46]

/**
 * Shuffles array in place.
 * @param {*} Array An array containing the items.
 */
function shuffle(a) {
    var j, x, i;
    for (i = a.length - 1; i > 0; i--) {
        j = Math.floor(Math.random() * (i + 1));
        x = a[i];
        a[i] = a[j];
        a[j] = x;
    }
    return a;
}

/**
 * Determines if a set is a superset of another set.
 * source: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Set
 */
function isSuperset(set, subset) {
    for (let elem of subset) {
        if (!set.has(elem)) {
            return false
        }
    }
    return true
}


/**
 * 
 * @param {*} json_logic contains logic for chest locations
 * @param {*} chest_contents_list list of every chest item in the game
 */
function randomize(json_logic, chest_contents_list) {
    const chest_contents_copy = [...chest_contents_list];
    const json_file = JSON.parse(JSON.stringify(json_logic)); // deep copy so original isn't modified
    shuffle(chest_contents_copy); // shuffle chest items
    for (const location in json_file) {
        for (const zmb in json_file[location]) {
            for (const object of json_file[location][zmb]) {
                object.object_metadata.chest_item_id = chest_contents_copy.pop().toString();
            }
        }
    }
    return json_file;
}


function hasItems(required_items, current_inventory) {
    for (const items of required_items) {
        let current_items_work = true;
        for (const item of items) {
            if (!current_inventory.has(item)) {
                current_items_work = false;
                break;
            }
        }
        if (current_items_work) {
            return true;
        }
    }
    return false;
}

/**
 * 
 * @param {*} required_to_defeat 
 * @param {*} current_inventory 
 * @param {*} enemies_conversion object mapping enemies to an array of items that can defeat them
 */
function canDefeat(enemies, current_inventory, enemies_conversion) {
    for (const enemy of enemies) {
        let defeatable = false;
        const items_can_defeat = enemies_conversion[enemy]; // get list of items that can defeat this enemy
        if (!items_can_defeat || items_can_defeat.length === 0) {
            // throw new Error(`Enemy ${enemy} not found!!!`);
            // TODO: finish enemy list, uncomment above line, remove below line
            return true; // for now, assume the enemy can be defeated
        }
        for (const items of items_can_defeat) {
            let defeatable_with_these_items = true;
            for (const item of items) {
                if (!current_inventory.has(item)) {
                    defeatable_with_these_items = false;
                    break;
                }
            }
            if (defeatable_with_these_items) {
                defeatable = true;
            }
        }
        if (!defeatable) {
            return false;
        }
    }
    return true;
}

/**
 * 
 * @param {*} seed_json Randomized game in JSON format
 * @param {*} defeatable_json JSON file specifying what item each enemy in the game can be killed with
 * @param {*} needed_to_win array of items needed make a seed valid (i.e. items needed to win the game)
 * @param {*} num_of_chests number of chests in the game
 */
function isValidSeed(seed_json, defeatable_json, needed_to_win, num_of_chests) {
    const inventory = new Set();
    const inventory_uids = new Set();
    let inventory_count = 0;
    let explored = new Set();
    let explored_count = 0;
    while (!isSuperset(inventory, needed_to_win)) {
        for (const location in seed_json) {
            for (const zmb in seed_json[location]) {
                for (const object of seed_json[location][zmb]) {
                    if (inventory_count + explored.size === chest_contents_list.length) { // TODO: figure out proper way to stop?
                        return false;
                    }
                    if (object.done) {
                        continue;
                    }
                    explored.add(object.universal_id);
                    if (!object.required) {
                        inventory.add(object.object_metadata.chest_item_id);
                        inventory_uids.add(object.universal_id);
                        inventory_count++;
                        explored = new Set();
                        object.done = true;
                        break;
                    }
                    const items_needed = object.required.map(obj => obj.items).filter(item => item);
                    const enemies_defeatable = object.required.map(obj => obj.defeatable).filter(item => item);;
                    const dungeon_accessible = object.required.dungeon_access;//.map(obj => obj.dungeon_access);
                    if (items_needed && items_needed.length > 0 && !hasItems(items_needed, inventory)) {
                        continue;
                    }
                    if (enemies_defeatable && !canDefeat(enemies_defeatable, inventory, defeatable_json)) {
                        continue;
                    }
                    // TODO: implement dungeon accessible logic
                    if (object.object_metadata) {
                        inventory.add(object.object_metadata.chest_item_id);
                        inventory_uids.add(object.universal_id);
                        inventory_count++;
                        explored = new Set();
                        // console.log(`Got ${object.object_metadata.chest_item_id}!!!`)
                        object.done = true;
                        break;
                    }
                }
            }
        }
    }
    return true;
}


const { mapItemNamesToIds } = require('./json/json_utilities');
const chests_json = mapItemNamesToIds(require('./json/chests'));
const defeatable_enemies = require('./json/enemies.json');
const item_to_id_mapping = require('./json/item_to_id.json');


const needed_to_win = new Set(['3', '7', '8', '12', '14']); // TODO: move this to external file, actually list items needed to beat game

let randomized_json;
let invalid_count = 0;
let valid_count = 0;
const iterations = 10000;
for (let i = 0; i < iterations; i++) {
    randomized_json = randomize(chests_json, chest_contents_list);
    if (!isValidSeed(randomized_json, defeatable_enemies, needed_to_win, item_to_id_mapping)) {
        // fs.writeFileSync(`temp/${Date.now()}.json`, JSON.stringify(randomized_json, null, '\t'));
        invalid_count++;
    }
    valid_count++;
}

function generateSeed() {
    let randomized_json;
    do {
        console.log('checking...')
        randomized_json = randomize(chests_json, chest_contents_list);
    } while (!isValidSeed(randomized_json, defeatable_enemies, needed_to_win, item_to_id_mapping));
    return randomized_json;
}

module.exports = {
    generateSeed
}