const { route } = require('./auth-routes');
const Client  = require('pg').Client;
const router = require('express').Router();


const authCheck = (req, res, next) => {
    if (!req.user) {
        // if user is not logged in
        res.redirect('/auth/login');
        console.log('unauthorized user.')
    } else {
        // if logged in
        next();
    }
};



const is_numeric = (str) => {
    return /^\d+$/.test(str);
};


// Your API method here

async function getSomething(figureId) {
    const client = new Client({
        user: 'username',
        host: '127.0.0.1',
        database: 'dbname',
        password: 'password',
        port: 5432,
      });
    client.connect();
    let result = await client.query(`YOUR SQL HERE`).catch(e => console.error(e.stack));
        
    client.end();
    if (result === undefined) {
        return {success: false};
    } else {
        console.log(1111);
        return {success: true, data: result.rows, count: result.rowCount};
    }
}


async function postSomething(user, params) {
    const client = new Client({
        user: 'username',
        host: '127.0.0.1',
        database: 'dbname',
        password: 'password',
        port: 5432,
      });
    client.connect();
    let query = await client.query(`YOUR SQL HERE`, [ params ]).catch(e => console.error(e.stack));
        
    if (query !== undefined) {
        let result = await client.query(`YOUR SQL HERE`).catch(e => console.error(e.stack));
        client.end();
        if (result === undefined) {
            return {success: false};
        } else {
            return {success: true, data: result.rows};
        }
    }
}

async function deleteSomething(user, params) {
    const client = new Client({
        user: 'username',
        host: '127.0.0.1',
        database: 'dbname',
        password: 'password',
        port: 5432,
      });
    client.connect();
    let query = await client.query(`YOUR SQL HERE`).catch(e => console.error(e.stack));
    client.end();
    if (query === undefined) {
        return {deleted: false};
    } else {
        return {deleted: true};
    }
}

async function updateSomething(user, params) {
    const client = new Client({
        user: 'username',
        host: '127.0.0.1',
        database: 'dbname',
        password: 'password',
        port: 5432,
      });
    client.connect();
    let query = await client.query(`YOUR SQL HERE`).catch(e => console.error(e.stack));
        
        client.end();
        if (query === undefined) {
            return {updated: false};
        } else {
            return {updated: true};
        }
        
}

// Your API route here
router.get('/anything', (req, res) => {
    // parse the query string or something
    getSomething(param).then((result) => {
        if (!req.user) {
            result.user = null;
        } else {
            result.user = Object.assign({}, {id: req.user.id, name: undefined, username: req.user.username, thumbnail: req.user.thumbnail}) ;
        }
        res.status(200).send(result);
    });
});

router.post('/anything', authCheck, (req, res) => {
    // parse the query string or something
    postSomething(req.user, params).then((result) => {
        res.status(200).send(result);
    });
});

router.delete('/anything', authCheck, (req, res) => {
    // parse the query string or something
    deleteSomething(req.user, params).then((result) => {
        res.status(200).send(result);
    });
});

router.put('/anything', authCheck, (req, res) => {
    // parse the query string or something
    updateSomething(req.user, params).then((result) => {
        res.status(200).send(result);
    });
});

router.get('/user/isauthorized', (req, res) => {
    let user = Object.assign({}, {id: req.user.id, name: undefined, username: req.user.username, thumbnail: req.user.thumbnail});
    res.send(user || { username: null});
});


module.exports = router;