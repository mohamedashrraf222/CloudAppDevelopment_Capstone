/**
 * Get all databases
 * Note that this script file is't working because cloudant.db.list() method returns a promise and IBM Cloud Function does not wait for this promise to get resolved. It immediately returns an empty object to the caller.
 * it will be fixed using promises
 */


const { CloudantV1 } = require("@ibm-cloud/cloudant");
const { IamAuthenticator } = require("ibm-cloud-sdk-core");


function main(params) {
  
  const i_am_api_key = params.IAM_API_KEY == "" ? process.env.IAM_API_KEY : params.IAM_API_KEY;
  const couch_username = params.COUCH_USERNAME == "" ? process.env.COUCH_USERNAME : params.COUCH_USERNAME;
  const couch_url = params.COUCH_URL == "" ? process.env.COUCH_URL : params.COUCH_URL;
  
  const authenticator = new IamAuthenticator({
    apikey: i_am_api_key,
  });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl(couch_url);

  let dbList = getDbs(cloudant);
  return { dbs: dbList };
}

function getDbs(cloudant) {
  let dbList = []
  cloudant
    .getAllDbs()
    .then((body) => {
      body.result.forEach((db) => {
        console.log(db);
        dbList.push(db);
      });
    })
    .catch((err) => {
      console.log(err);
    });

    return dbList
}

const params = {
  "COUCH_URL": "",
  "IAM_API_KEY": "",
  "COUCH_USERNAME": ""
}
console.log(main(params));