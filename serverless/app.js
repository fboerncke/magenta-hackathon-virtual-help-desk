"use strict";

// eslint-disable-next-line import/no-unresolved

const Airtable = require("airtable");
const express = require("express");
const app = express();

/**
 * Business Logic:
 * process input parameter and return result as json
 */

app.get("/lookup", async (request, response) => {
  // Define database connection
  Airtable.configure({ apiKey: "keyXXXXXXXXXX" }); // values are XXXXed
  const base = Airtable.base("appXXXXXXXXXX"); // values are XXXXed
  const table = base("LookupTable");

  await table
    .select({
      view: "Grid view",
    })
    .firstPage((err, records) => {
      try {
        // max 100 entries on page - should be enough for the demo case
        if (err) {
          console.error(err);
          return;
        }

        let parameter = request.query.parameter.toLowerCase();

        let filteredResult = [];

        // iterate table and select one appropriate result
        records.forEach((elementFromDatabase) => {
          if (
            isMatch(parameter, elementFromDatabase) &&
            filteredResult.length === 0 // only one element in result
          ) {
            filteredResult.push({
              id: elementFromDatabase.id,
              keys: elementFromDatabase.get("keys"),
              explanation: elementFromDatabase.get("explanation"),
              informationUrl: elementFromDatabase.get("informationUrl"),
              contactName: elementFromDatabase.get("contactName"),
              contactData: elementFromDatabase.get("contactData"),
            });
          }
        });

        if (
          parameter !== undefined &&
          parameter.length > 0 &&
          filteredResult.length === 0
        ) {
          // the search expression not found yet: create a new entry in DB
          table.create(
            {
              keys: parameter,
              explanation:
                "!!! Nach diesem Begriff wurde gesucht, aber bis jetzt gibt es dafür noch keine passende Antwort im System.",
            },
            (err, record) => {
              if (err) {
                console.error(err);
                response.json({
                  searchterm,
                  filteredResult: [],
                  status: "ERROR IN BACKEND",
                });
              }
            }
          );
        }
        let searchterm = parameter;

        // express helps us take JavaScript objects and send them as JSON
        if (filteredResult.length === 0) {
          response.json({
            searchterm,
            filteredResult,
            status: "ENTRY NOT FOUND - ADDED IN BACKEND",
          });
        } else {
          response.json({ searchterm, filteredResult, status: "OK" });
        }
      } catch (error) {
        console.log("######");
        console.log({ error });
        response.json({
          searchterm,
          filteredResult: [],
          status: "ERROR IN BACKEND",
        });
      }
    });
});

/**
 * Check if search expression is a hard match
 */
function isMatch(searchExpression, elementFromDatabase) {
  let keys = elementFromDatabase.get("keys");
  if (keys !== undefined) {
    let keyArray = keys.split(",");

    for (const key of keyArray) {
      if (
        searchExpression === key.trim().toLowerCase() &&
        elementFromDatabase.get("isActive") === true
      ) {
        return true;
      }
    }
  }
  return false;
}

/**
 * listen for requests
 */
const listener = app.listen(process.env.PORT, () => {
  console.log("Your app is listening on port " + listener.address().port);
});

module.exports = app;
