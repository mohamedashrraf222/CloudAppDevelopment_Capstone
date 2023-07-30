const { CloudantV1 } = require("@ibm-cloud/cloudant");
const { IamAuthenticator } = require("ibm-cloud-sdk-core");

async function main(params) {
  const i_am_api_key = "CdwObnLdugcpE7PNQGxwV-JTH3i7w7yyG6ifp77RGmE2";
  const couch_username = "894cec5b-94ad-47e3-a6a1-715fd7a8db9b-bluemix";
  const couch_url =
    "https://894cec5b-94ad-47e3-a6a1-715fd7a8db9b-bluemix.cloudantnosqldb.appdomain.cloud";

  const authenticator = new IamAuthenticator({ apikey: i_am_api_key });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl(couch_url);

  let filtered = {};

  if (params) {
    filtered = params;
    filtered["__ow_headers"] && delete filtered.__ow_headers;
    filtered["__ow_method"] && delete filtered.__ow_method;
    delete filtered[Object.keys(filtered)[0]]
  }

  if (params && Object.keys(filtered).length > 0) {
    try {
      let dbList = await cloudant.postFind({
        db: "dealerships",
        selector: filtered,
      });
      let documents = dbList.result.docs;
      return {
        statusCode: 200,
        headers: {
          "Content-Type": "application/json",
        },
        body: documents,
      };
    } catch (error) {
      return { error: error };
    }
  } else {
    try {
      let dbList = await cloudant.postAllDocs({
        db: "dealerships",
        includeDocs: true,
      });
      let documents = dbList.result.rows.map((row) => row.doc);
      return {
        statusCode: 200,
        headers: {
          "Content-Type": "application/json",
        },
        body: documents,
      };
    } catch (error) {
      return { error: error.description };
    }
  }
}

let myparamss = {
  __ow_headers: {
    accept:
      "text/html, application/xhtml+xml, application/xml;q=0.9, image/webp, image/apng, */*;q=0.8, application/signed-exchange; v=b3;q=0.7",
    "accept-encoding": "gzip, deflate, br",
    "accept-language": "en-US, en;q=0.9, ar;q=0.8",
    "cache-control": "max-age=0",
    host: "us-south.functions.appdomain.cloud",
    "sec-ch-ua":
      '"Not.A/Brand";v="8", "Chromium";v="114", "Microsoft Edge";v="114"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent":
      "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.58",
    "x-forwarded-for": "172.71.186.220",
    "x-forwarded-host": "us-south.functions.appdomain.cloud",
    "x-forwarded-port": "443",
    "x-forwarded-proto": "https",
    "x-forwarded-scheme": "https",
    "x-real-ip": "172.71.186.220",
    "x-request-id": "20956be4121d66b1ec4f5b674ebf7750",
    "x-scheme": "https",
  },
  __ow_method: "get",
  __ow_path: "hello",
  state: "Georgia",
};
main({state: 'Georgia'}).then((res) => console.log(res));
