# GraphQL Api for fetching Country Details
This project is a GraphQL API which is used to fetch details of countries. The API is written in Python 3 and was built using Falcon framework and Graphene for GraphQL. Usage is given below.

### Requirements
- Docker
- Docker Compose
### Starting the API
Run the following command to initialize the API inside docker
```shell
docker-compose up
```
Once the containers have been started, goto http://localhost/graphql to access the API. Note
that there is no page configured to handle GET requests. So you have to use a GraphQL explorer to play with the API. I was using Altair Graphql Client extension for browser.

Once you have opened the explorer of your choice you can start querying the API. The API supports the following operations
1. List Countries ( Query )
2. List Countries By Language ( Query )
3. List Countries Near a Location Coordinate ( Query )
4. Country details ( Query )
5. Update Country ( Mutation )

Types available

**Country**

Country is the main object type available in the API. The Country object type supports the following fields:

```graphql
country {
	id
    commonName
    officialName
    independent
    unMember
    languages
    location{
      coordinates
    }
    area
    region
    subregion
    currencies{
      edges {
        node {
          name
          shortName
          symbol
        }
      }
    }
  }
```


#### List countries
Type: Query 

The API returns a list of all countries available in the database. The API supports pagination through optional variables that can be provided. 

Example Query:
```graphql
query listCountries($page: Int = 0, $limit: Int = 20){
  countries(page: $page, limit: $limit){
    id
    commonName
    languages
    location{
      coordinates
    }
    unMember
  }
}
```
Variables
```json
variables = {
  "page": 0,
  "limit": 20
}
```

####  List Countries By Language
Type : Query

The API allows you to filter the results using any language available. 

Example Query
```graphql
query filterCountriesByLanguage($language: String!, $page: Int, $limit: Int){
  countriesByLanguage(language: $language, page: $page, limit: $limit){
    id
    commonName
    officialName
    languages
  }
}
```
Variables
```json
{
  "language": "Hindi",
  "limit": 20
}
```

#### List Countries Near By a location coordinate
Type : Query

The API allows you to find nearby countries based on a location coordinate as input. It makes use of Geospatial querying capablities of MongoDB.

Example Query
```graphql
query filterCountriesNearCoordinate($lat: Float!, $long: Float!, $range: Int!, $page: Int, $limit: Int) {
  countriesNearLocation(lat: $lat, long: $long, range: $range, page: $page, limit: $limit){
    commonName
    officialName
    location{
      coordinates
    }
  }
}
```
Variables
```json
{
  "lat": 37.0902,
  "long": -95.7129,
  "range": 2000000
}
```

#### Country Details
Type: Query

You can fetch the details of a single country using it's ID provided in the listing requests.

Example Query
```graphql

query countryById($id: String!){
  country (id: $id) {
    commonName
    officialName
    languages
    independent
    unMember
    area
  }
}
```
Variables
```json
{
  "id": "Q291bnRyeTo2MzM5YTU3NDdjMzNlNTJiNTczZjliZDg="  // ID should be modified
}
```

#### Update Country
Type: Mutation

Allows you to edit the details of a Country. You can edit the following properties of a country.
1. independent
2. unMember
3. languages
4. area

You should provide required parameter ID and atleast one of the above four fieds for the updation to work.

Example Query
```graphql
mutation updateCountry($id: String!, $independent: Boolean, $unMember: Boolean, $area: Int, $languages: [String], $language: String) {
  updateCountry(id_: $id, independent: $independent, unMember: $unMember, area: $area, languages: $languages, language: $language){
    success
    country {
      id
      commonName
      officialName
      independent
      unMember
      area
      languages
    }
  }
}
``` 

Variables
```json
{
  "id": "Q291bnRyeTo2MzM5YTU3NDdjMzNlNTJiNTczZjliZDg=", // ID should be modified
  "unMember": false,
  "independent": false
}
```


