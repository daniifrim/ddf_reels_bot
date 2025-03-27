const fs = require('fs');
const { execSync } = require('child_process');
const dotenv = require('dotenv');

// Load environment variables from .env file
const envConfig = dotenv.parse(fs.readFileSync('.env'));

// Variables to update
const keysToUpdate = [
  'CODA_API_KEY',
  'CODA_DOC_ID',
  'CODA_TABLE_ID',
  'CODA_LINK_COLUMN_ID',
  'TELEGRAM_BOT_TOKEN'
];

console.log('Starting Vercel environment variable update...');

// Update each environment variable
keysToUpdate.forEach(key => {
  const value = envConfig[key];
  
  if (!value) {
    console.log(`⚠️ Skipping ${key} - not found in .env file`);
    return;
  }
  
  try {
    // Remove existing variable (if it exists)
    try {
      console.log(`Removing existing ${key}...`);
      execSync(`vercel env rm ${key} production -y`, { stdio: 'inherit' });
    } catch (error) {
      console.log(`Variable ${key} not found or could not be removed. Continuing...`);
    }
    
    // Add the new variable using a different approach
    console.log(`Adding ${key}...`);
    const cmd = `echo "${value}" | vercel env add ${key} production`;
    execSync(cmd, { stdio: 'inherit' });
    
    console.log(`✅ Successfully updated ${key}`);
  } catch (error) {
    console.error(`❌ Error updating ${key}: ${error.message}`);
  }
});

console.log('Environment variables update completed!');
console.log('Run "vercel --prod" to redeploy with the new variables.'); 