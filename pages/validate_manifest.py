const fs = require('fs');
const path = require('path');

const manifestPath = path.join(__dirname, 'manifest.json');

// Required fields for Farcaster Mini App
const requiredFields = {
  name: 'string',
  description: 'string',
  version: 'string',
  iconUrl: 'string',
  homeUrl: 'string',
  developer: {
    name: 'string',
    url: 'string'
  }
};

function validateType(value, expectedType) {
  return typeof value === expectedType;
}

function validateManifest(manifest) {
  let isValid = true;

  for (const [key, expected] of Object.entries(requiredFields)) {
    if (!(key in manifest)) {
      console.warn(`⚠️ Missing field: ${key}`);
      isValid = false;
    } else if (typeof expected === 'object') {
      for (const [subKey, subType] of Object.entries(expected)) {
        if (!(subKey in manifest[key])) {
          console.warn(`⚠️ Missing subfield: ${key}.${subKey}`);
          isValid = false;
        } else if (!validateType(manifest[key][subKey], subType)) {
          console.warn(`⚠️ Incorrect type for ${key}.${subKey}. Expected ${subType}`);
          isValid = false;
        } else {
          console.log(`✔️ ${key}.${subKey} is valid`);
        }
      }
    } else if (!validateType(manifest[key], expected)) {
      console.warn(`⚠️ Incorrect type for ${key}. Expected ${expected}`);
      isValid = false;
    } else {
      console.log(`✔️ ${key} is valid`);
    }
  }

  return isValid;
}

try {
  const raw = fs.readFileSync(manifestPath, 'utf-8');
  const manifest = JSON.parse(raw);
  console.log('✅ Manifest loaded successfully\n');

  const result = validateManifest(manifest);
  if (result) {
    console.log('\n🎉 Manifest is valid!');
  } else {
    console.log('\n❌ Manifest has issues. Fix them before deploying.');
  }
} catch (err) {
  console.error(`❌ Error reading or parsing manifest: ${err.message}`);
}
