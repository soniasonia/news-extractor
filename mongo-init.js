db.auth('root', 'secret')

db = db.getSiblingDB('simple-app')

db.createUser(
        {
            user: "user",
            pwd: "pass",
            roles: [
                {
                    role: "readWrite",
                    db: "simple-app"
                }
            ]
        }
);
