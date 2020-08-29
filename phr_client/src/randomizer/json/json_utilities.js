
/* eslint-disable */


const fs = require('fs');

// const chests = require('./chests_v3.json');
const chests = require('./chests_v5.json');
const item_to_id_mapping = require('./item_to_id.json');

function generateUniversalIds(chests, versionNumber) {
    for (map in chests) {
        for (narcFile in chests[map]) {
            for (zmbFile in chests[map][narcFile]) {
                for (object of chests[map][narcFile][zmbFile]) {
                    object.universal_id = `${zmbFile.substring(0, zmbFile.indexOf('.zmb'))}_${object.location.substring(2)}`;
                }
            }
        }
    }
    const jsonFileName = `chests_v${versionNumber}.json`;
    if (fs.existsSync(jsonFileName)) {
        console.log(`[ERROR] File "${jsonFileName}" already exists.`);
        return;
    }
    fs.writeFileSync(`chests_v${versionNumber}.json`, JSON.stringify(chests, null, 2), 'utf8');
}


// use for json that doesn't have narc file name
function generateUniversalIds2(chests, versionNumber) {
    for (map in chests) {
        for (zmbFile in chests[map]) {
            for (object of chests[map][zmbFile]) {
                object.universal_id = `${zmbFile.substring(0, zmbFile.indexOf('.zmb'))}_${object.location.substring(2)}`;
            }
        }
    }
    const jsonFileName = `chests_v${versionNumber}.json`;
    if (fs.existsSync(jsonFileName)) {
        console.log(`[ERROR] File "${jsonFileName}" already exists.`);
        return;
    }
    fs.writeFileSync(`chests_v${versionNumber}.json`, JSON.stringify(chests, null, 2), 'utf8');
}

// Recursively remove empty JSON documents
function cleanUp(obj) {
    for (const key in obj) {
        const value = obj[key];
        if (typeof(value) === "object") {
            cleanUp(value);
        } else if((!value || value.length === 0) && value !== 0) {
            delete obj[key];
        }
    }
}

const removeEmpty = (obj) => {
    Object.entries(obj).forEach(([key, val])  =>
      (val && typeof val === 'object') && removeEmpty(val) ||
      (val === null || val === "") && delete obj[key]
    );
    return obj;
  };

// function serializeJson(chestsJson) {

// }
// removeEmpty(chests);
// generateUniversalIds2(chests, 5);

const locationMapping = require('./location_mapping.json');

function generateLogicTemplate(chests) {
    for (map in chests) {
        for (zmbFile in chests[map]) {
            const split = zmbFile.split('_')
            const number = split[split.length - 1].substring(0, 2);
            split.pop();
            const location = locationMapping[split.join('_')];
            
            console.log(`${location}:`);
            for (object of chests[map][zmbFile]) {
                // object.universal_id = `${zmbFile.substring(0, zmbFile.indexOf('.zmb'))}_${object.location.substring(2)}`;
                // console.log(object);
                const id = object.universal_id;
                const chestType = object.object_type;
                console.log(`\tChest Type: ${chestType}`);
                console.log(`\tArea #: ${Number(number)}`);
                console.log(`\tUID: ${id}`);
                console.log('\n');
            }
        }
    }
}


function mapItemNamesToIds(chests_json) {
    for (map in chests) {
        for (zmbFile in chests[map]) {
            for (object of chests[map][zmbFile]) {
                if (!object.required) {
                    continue;
                }
                for (requirement of object.required) {
                    if (requirement.items) {
                        // console.log(requirement.items);
                        requirement.items = requirement.items.map(item => item_to_id_mapping[item]);
                    }
                }
            }
        }
    }
    return chests_json;
}


module.exports = {
    mapItemNamesToIds
}