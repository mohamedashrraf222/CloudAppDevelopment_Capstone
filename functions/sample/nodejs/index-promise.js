/**
 * Get all dealerships
 * but this script still have a bug because it returns a promis and the main function is't async function
 */

const { CloudantV1 } = require('@ibm-cloud/cloudant');
const { IamAuthenticator } = require('ibm-cloud-sdk-core');




function main(params) {

    const i_am_api_key = params.IAM_API_KEY == "" ? process.env.IAM_API_KEY : params.IAM_API_KEY;
    const couch_username = params.COUCH_USERNAME == "" ? process.env.COUCH_USERNAME : params.COUCH_USERNAME;
    const couch_url = params.COUCH_URL == "" ? process.env.COUCH_URL : params.COUCH_URL;

    const authenticator = new IamAuthenticator({ apikey: i_am_api_key })
    const cloudant = CloudantV1.newInstance({
      authenticator: authenticator
    });
    cloudant.setServiceUrl(couch_url);

    let dbListPromise = getDbs(cloudant);
    return dbListPromise;
}

function getDbs(cloudant) {
     return new Promise((resolve, reject) => {
         cloudant.getAllDbs()
             .then(body => {
                 resolve({ dbs: body.result });
             })
             .catch(err => {
                  console.log(err);
                 reject({ err: err });
             });
     });
 }
 
 
 /*
 Sample implementation to get the records in a db based on a selector. If selector is empty, it returns all records. 
 eg: selector = {state:"Texas"} - Will return all records which has value 'Texas' in the column 'State'
 */
 function getMatchingRecords(cloudant,dbname, selector) {
     return new Promise((resolve, reject) => {
         cloudant.postFind({db:dbname,selector:selector})
                 .then((result)=>{
                   resolve({result:result.result.docs});
                 })
                 .catch(err => {
                    console.log(err);
                     reject({ err: err });
                 });
          })
 }
 
                        
 /*
 Sample implementation to get all the records in a db.
 */
 function getAllRecords(cloudant,dbname) {
     return new Promise((resolve, reject) => {
         cloudant.postAllDocs({ db: dbname, includeDocs: true, limit: 10 })            
             .then((result)=>{
               resolve({result:result.result.rows});
             })
             .catch(err => {
                console.log(err);
                reject({ err: err });
             });
         })
 }

 const params = {
    "COUCH_URL": "",
    "IAM_API_KEY": "",
    "COUCH_USERNAME": ""
  }

  console.log( main(params));
