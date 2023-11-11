from bson.objectid import ObjectId

from core.database import MongoDBConnector

from exceptions.user_exceptions import UserNotFoundException, UserAlreadyExistsException, DisplayNameExistException, PasswordsDoNotMatchException, UserNotFoundException, PasswordsMatchException, UserIdNotFoundException
from models.user import UserModel, UserDatabaseInModel, UserDatabaseOutModel
from services.auth_services import AuthenticationServices
from utils.hasher import hash_password

# Get singleton db connection 
user_db_collection = MongoDBConnector.get_client()["dishswapdb"]["users"] 


class UserServices():
    def check_if_passwords_match(self, password: str, confirm_password: str):
        if password != confirm_password: raise PasswordsDoNotMatchException


    def check_if_passwords_not_match(self, current_password: str, new_password: str):
        if current_password == new_password: raise PasswordsMatchException

    
    async def check_user_exist(self, email: str, display_name: str):
        try:
            query = {}

            if email:
                query["$or"] = [{"email": email}]
            if display_name:
                query["$or"].append({"display_name": display_name})

            user_doc = await user_db_collection.find_one(query)

            if user_doc is not None:
                raise UserAlreadyExistsException
            
        except Exception as e:
            raise


    async def check_if_display_name_exists(self, display_name: str):
        try:
            print(display_name)
            # Check if the display_name exists in the database
            result = await user_db_collection.count_documents({"display_name": display_name})
            print(result)
            if result > 0:
                raise DisplayNameExistException(display_name)            
            
        except Exception as e:
            raise


class User(): 

    user_services =  UserServices()

    def __init__(self, user_model: UserModel = None): 
        self.__id = getattr(user_model, 'id', None)
        self.__email = getattr(user_model, 'email', None)
        self.__display_name = getattr(user_model, 'display_name', None)
        self.__hashed_password = getattr(user_model, 'hashed_password', None)
        self.__user_type = getattr(user_model, 'user_type', "user")
        self.__password = getattr(user_model, 'password', None)
        self.__confirm_password = getattr(user_model, 'confirm_password', None)
        self.__current_password = getattr(user_model, 'current_password', None)
        self.__new_password = getattr(user_model, 'new_password', None)

 
    # Getter methods 
    def get_id(self): 
        return self.__id 
     
    def get_email(self): 
        return self.__email 
 
    def get_display_name(self): 
        return self.__display_name 
     
    def get_hashed_password(self): 
        return self.__hashed_password 
     
    def get_user_type(self): 
        return self.__user_type 
 
    # Setter methods 
    def set_id(self, new_id): 
        self.__id = new_id

    def set_email(self, new_email): 
        self.__email = new_email 
 
    def set_display_name(self, new_display_name): 
        self.__display_name = new_display_name 
 
    def set_hashed_password(self, new_hashed_password): 
        self.__hashed_password = new_hashed_password 
 
    def set_user_type(self, new_user_type): 
        self.__user_type = new_user_type


    # User Database Functions
    async def create_user(self) -> bool:
        try:
            self.user_services.check_if_passwords_match(self.__password, self.__confirm_password)

            await self.user_services.check_user_exist(self.__email, self.__display_name)
            
            self.__hashed_password = hash_password(self.__password)
        
            user_database_in_model = UserDatabaseInModel(
                                        email=self.__email,
                                        display_name=self.__display_name,
                                        user_type=self.__user_type,
                                        hashed_password=self.__hashed_password
                                    )
            result = await user_db_collection.insert_one(user_database_in_model.model_dump())

            if result:
                return True

            return False
        except Exception as e:
            raise
    

    async def get_user_by_id(self) -> None:
        try:
            user = await user_db_collection.find_one({"_id": ObjectId(self.__id)})
            
            if user:
                user["_id"] = str(user["_id"])
                
                user_database_out_model = UserDatabaseOutModel(**user)

                self.__email = user_database_out_model.email
                self.__display_name = user_database_out_model.display_name
                self.__hashed_password = user_database_out_model.hashed_password

                return
            
            raise UserNotFoundException()
        
        except Exception as e:
            raise

    
    async def get_user_by_email(self) -> None:
        try:
            user = await user_db_collection.find_one({"email": self.__email})
            
            if user:
                user["_id"] = str(user["_id"])
                
                user_database_out_model = UserDatabaseOutModel(**user)

                self.__id = user_database_out_model.id
                self.__display_name = user_database_out_model.display_name
                self.__hashed_password = user_database_out_model.hashed_password

                return
            
            raise UserNotFoundException()
        
        except Exception as e:
            raise
    

    async def update_password(self):
        try:
            self.user_services.check_if_passwords_not_match(self.__current_password, self.__new_password)

            AuthenticationServices().validate_password(self.__current_password, self.__hashed_password)

            self.__hashed_password = hash_password(self.__new_password)

            result = await user_db_collection.update_one(
                {"_id": ObjectId(self.__id)},
                {"$set": {
                    "hashed_password": self.__hashed_password
                    }
                }
            )
            
            # Check if the update was successful
            if result.modified_count > 0:
                return True
            else:
                raise UserIdNotFoundException(id)
                
        except Exception as e:
            raise


    async def update_display_name(self):
        try:
            print(self.__display_name)
            await self.user_services.check_if_display_name_exists(self.__display_name)

            result = await user_db_collection.update_one(
                {"_id": ObjectId(self.__id)},
                {"$set": {
                    "display_name": self.__display_name
                    }
                }
            )
            
            # Check if the update was successful
            if result.modified_count > 0:
                return True
            else:
                raise UserIdNotFoundException()
                
        except Exception as e:
            raise