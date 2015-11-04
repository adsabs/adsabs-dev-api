# ADS Bibliographic Libraries API

The source code of this microservice can be viewed [here](https://github.com/adsabs/biblib-service).

## API end point
`https://api.adsabs.harvard.edu/v1/biblib`

### End points and methods

#### /libraries

End point to create a library or view all libraries for a given user.

##### GET
Obtains all the libraries that belong to the requesting user, along with some additional metadata.

*Return data*:
  * name:
  	* **string**
  	* Name of the library
  * id:
  	* **string**
  	* ID of the library
  * description:
  	* **string**
  	* Description of the library
  * num_documents:
  	* **int**
  	* Number of documents in the library
  * date_created:
  	* **string**
  	* ISO date library was created
  * date_last_modified:
  	* **string**
  	* ISO date library was last modified
  * permission:
  	* **string**
  	* Permission type, can be: 'read', 'write', 'admin', or 'owner'
  * public:
  	* **boolean**
  	* True means it is a public library
  * num_users:
  	* **int**
  	* Number of users with permissions to this library
  * owner:
  	* **string**
  	* Identifier of the user who created the library

*Permissions*:
Must be authenticated via the API.

##### POST
Creates a library for the requesting user. Returns metadata on the library created.

*Post body*:
  * *name*:
  	* **string**
  	* name of the library (must be unique for that user)
  * *description*:
  	* **string**
  	* description of the library
  * *public*:
  	* **boolean**
  	* is the library public to view
  * *bibcode (OPTIONAL)*:
  	* **list**
  	* list of bibcodes to add

*Return data*:
  * **name**:
  	*<string>    Name of the library
  * **id**:
  	* <string>
  	* ID of the library
  * **description**:
  	* <string>
  	* Description of the library

*Permissions*:
Must be authenticated via the API.

#### /libraries/&lt;library_id&gt;

End point to interact with a specific library, only returns library content if the user has the correct privileges. See the document end point for deleting a library.

  * **library_id** [**string**] is the unique identifier of the library, as specified in the `/libraries` GET response.

##### GET
Obtains all the documents of a given library.

*Return data*:

  * documents:
  	* **list**
  	* Currently, a list containing the bibcodes.
  * solr:
  	* **dict**
  	* The response from the solr bigquery end point
  * metadata:
  	* **dict**
  	* contains the following:
        * name:
        	* **string**
        	* Name of the library
        * id:
        	* **string**
        	* ID of the library
        * description:
        	* **string**
        	* Description of the library
        * num_documents:
        	* **int**
        	* Number of documents in the library
        * date_created:
        	* **string**
        	* ISO date library was created
        * date_last_modified:
        	* **string**
        	* ISO date library was last modified
        * permission:
        	* **sting**
        	* Permission type, can be: 'read', 'write', 'admin', or 'owner'
        * public:
        	* **boolean**
        	* True means it is public
        * num_users:
        	* **int**
        	* Number of users with permissions to this library
        * owner:
        	* **string**
        	* Identifier of the user who created the library
  * updates:
  	* **dict**
  	* contains the following
        * num_updated:
        	* **int**
        	* Number of documents modified based on the response from solr
        * duplicates_removed:
        	* **int**
        	* Number of files removed because they are duplications
        * update_list:
        	* **list**[**dict**]
        	*  List of dictionaries such that a single element described the original bibcode (key) and the updated bibcode now being stored (item)

*Permissions*:
The following type of user can read a library:
  - owner
  - admin
  - write
  - read

#### /documents/&lt;library_id&gt;

End point to interact with a specific library, by adding documents and removing documents. You also use this endpoint to delete the entire library.

  * **library_id** [**string**] is the unique identifier of the library, as specified in the `/libraries` GET response.

##### POST

Request that adds a document to a library for a given user.

*Post body*:

  * bibcode:
  	* **list**
  	* List of bibcodes to be added
  * action:
  	* **string**
  	* 'add' or 'remove'
  		* add - adds a bibcode
  		*  remove - removes a bibcode

*Return data*:
  * number_added:
  	* **int**
  	* number of documents added (if 'add' is used)
  * number_removed:
  	* **int**
  	* number of documents removed (if 'remove' is used)

*Permissions*:
The following type of user can add documents:
  - owner
  - admin
  - write

##### PUT

Request that updates the meta-data of the library

*Post-body*:
  * name:
    * **string**
    * name of the library
  * description:
  	* **string**
  	* description of the library
  * public:
  	* **boolean**
  	* if the library should be publicly viewable

*Note: The above are optional. Leave fields out if they do not need to be updated.*

*Return data*:
  * name:
    * **string**
    * name of the library
  * description:
  	* **string**
  	* description of the library
  * public:
  	* **boolean**
  	* if the library should be publicly viewable

*Note: returns the key/value that was requested to be updated*

*Permissions*:
The following type of user can update the 'name', 'library', and 'public' attributes:
  - owner
  - admin

##### DELETE

Request that deletes a library.

*Permissions*:

The following type of user can update a library:
  - owner

#### /permissions/&lt;library_id&gt;

End point to manipulate the permissions between a user and a library.

  * **library_id** [**string**] is the unique identifier of the library, as specified in the `/libraries` GET response.

##### GET
Request that returns the permissions for a given library.

*Return data*:
  * list of dictionaries, where each dictionary is for a specific user. The dictionary contains a list of all the permissions of the user.
  	* **list**
  	* user dictionary
  		* **dict**
  			* **key**:
  				* **string**
  				* user e-mail
  			* **item**:
  				* **list**
  				* list of permissions: 'read', 'write', 'admin', 'owner'

*Permissions*:
The following type of user can access permissions of a library:
  - owner
  - admin

##### POST
Request that modifies the permissions of a library

*Post data*:

  * username:
  	* **string**
  	* specifies which user's permissions to be modified
  * permission:
  	* **string**
  	* 'read', 'write', 'admin' or 'owner'
  * value:
  	* **boolean**
	* whether the user has this permission (True=yes, False=no)


*Permissions*:
The following type of user can update a permission for a user for a given library:
  - owner
  - admin

#### /transfer/&lt;library_id&gt;

End point to transfer a the ownership of a library to another ADS user.

  * **library_id** [**string**] is the unique identifier of the library, as specified in the `/libraries` GET response.

##### POST
Request that transfers the ownership of a library from one user to another.

*Post body*:
  * transfer_user:
    * **string**
    * username of the user the account should be transfered to

*Permissions*:
The following type of user can transfer libraries:
  - owner

## Permissions
  * **owner**: Owns the library. Can read libraries, add/remove bibcodes, delete the library, add/remove permissions, transfer ownership of the library.
  * **admin**: Can read libraries, add/remove bibcodes, add/remove permissions.
  * **write**: Can read libraries, add/remove bibcdes.
  * **read**: Can read libraries.

Any other user that does not have a permission to the library they try to visit, can only see it if it is public. If the user has no permissions, they cannot view this library.
