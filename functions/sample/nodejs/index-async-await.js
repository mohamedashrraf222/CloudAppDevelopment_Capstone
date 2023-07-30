/**
 * Get all dealerships
 */

const { CloudantV1 } = require("@ibm-cloud/cloudant");
const { IamAuthenticator } = require("ibm-cloud-sdk-core");

async function main(params) {
  const i_am_api_key =
    params.IAM_API_KEY == "" ? process.env.IAM_API_KEY : params.IAM_API_KEY;
  const couch_username =
    params.COUCH_USERNAME == ""
      ? process.env.COUCH_USERNAME
      : params.COUCH_USERNAME;
  const couch_url =
    params.COUCH_URL == "" ? process.env.COUCH_URL : params.COUCH_URL;

  const authenticator = new IamAuthenticator({ apikey: i_am_api_key });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl(couch_url);
  try {
    let dbList = await cloudant.postAllDocs({
      db: "dealerships",
      includeDocs: true,
    });
    const documents = dbList.result.rows.map((row) => row.doc);
    return documents;
  } catch (error) {
    return { error: error.description };
  }
}

const params = {
  COUCH_URL: "",
  IAM_API_KEY: "",
  COUCH_USERNAME: "",
};
main(params).then((res) => console.log(res));
