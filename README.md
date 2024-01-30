## Vending machine API


# Requirements with comments:  
- REST API should be implemented consuming and producing “application/json” [X]
    - Done using FastAPI
- Implement product model with amountAvailable, cost (should be in multiples of 5), productName and sellerId fields [X]
    - Used Pydantic model with validator to make sure cost is multiples of 5
- Implement user model with username, password, deposit and role fields [X]
    - Done
- Implement an authentication method (basic, oAuth, JWT or something else, the choice is yours) [X]
    - JWT with access/refresh token
- All of the endpoints should be authenticated unless stated otherwise [X]  
    - Done  
- Implement CRUD for users (POST /user should not require authentication to allow new user registration)[X]
    - Update only password - do not allow changing roles 
    - Delete available for your own account only
    - In the future admin-role could do more  
- Implement CRUD for a product model (GET can be called by anyone, while POST, PUT and DELETE can be called only by the seller user who created the product)[X]
    - done
- Implement /deposit endpoint so users with a “buyer” role can deposit only 5, 10, 20, 50 and 100 cent coins into their vending machine account (one coin at the time)[X]
    - done
- Implement /buy endpoint (accepts productId, amount of products) so users with a “buyer” role can buy a product (shouldn't be able to buy multiple different products at the same time) with the money they’ve deposited. API should return total they’ve spent, the product they’ve purchased and their change if there’s any (in an array of 5, 10, 20, 50 and 100 cent coins)[X]
    - done
- Implement /reset endpoint so users with a “buyer” role can reset their deposit back to 0 [X]
    - done
- Take time to think about possible edge cases and access issues that should be solved [X]
    - One edge case - make sure vending machine has enough change
        - to do that we needed to record vending machine with state (can't use memory because there might be multiple uvicorn workers) - decided to use table in DB
        - in the future it should be relatively easy to introduce multiple vending machines with separate users and products
    - made sure to lock records before changing them, rollback when something fails


# BONUS: - Not implemented
- If somebody is already logged in with the same credentials, the user should be given a message "There is already an active session using your account". In this case the user should be able to terminate all the active sessions on their account via an endpoint i.e. /logout/all - To do that I'd have to save sessions - not enough time to implement that but there could be additional field added to JWT like `active-session` (that is a hash stored inside db, with extra info like ip etc.)
- Attention to security
