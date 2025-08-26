const express = require('express');
const multer = require('multer');
const cors = require('cors');

const app = express();

app.use(cors());

const PORT = process.env.PORT || 5000;

const storage = multer.diskStorage({
    destination:'uploads',
    filename:(req,file, cb) =>{
        cb(null, Date.now()+'_'+file.originalname);
    }
})

const upload = multer({storage})


app.post("/upload", upload.array('files'), (req, res, next) =>{
    res.status(200).json({msg:'success'});
});


app.listen(PORT, ()=>{
    console.log("Server listening on PORT", PORT);
})