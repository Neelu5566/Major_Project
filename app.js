const express = require('express');
const app = express();
const fs = require('fs');
const path = require('path');
const bodyParser = require('body-parser');
const Fraction = require('fraction.js');
const { createCanvas, registerFont, Canvas } = require('canvas');
const multer = require('multer');
const port = 3000;
const axios = require('axios');

// Set EJS as the view engine
app.set('view engine', 'ejs');

app.use(express.static(path.join(__dirname, 'public')));

app.use(bodyParser.urlencoded({ extended: false }));

// Define a route to render the EJS file
const storage = multer.diskStorage({
  destination: function (req, file, cb) {
    cb(null, 'uploads/');
  },
  filename: function (req, file, cb) {
    cb(null, file.fieldname + '-' + Date.now() + path.extname(file.originalname));
  }
});

// Initialize multer middleware
const upload = multer({ storage: storage });

app.get('/quiz', (req, res) => {
  // Read the JSON file
  const jsonData = fs.readFileSync('output.json', 'utf8');
  let entries
  // const entries = JSON.parse(jsonData);
  if (jsonData.length === 0) {
    // JSON file is empty, return 0
    console.log('JSON file is empty');
    return res.render('index', { entries: 0 });
  }
  else {

    try {
      entries = JSON.parse(jsonData);
      return res.render('index', { entries });
    } catch (error) {
      console.error('Error parsing JSON:', error);

    }

  }
});




app.post('/submit', (req, res) => {
  const inputData = req.body;

  const name = inputData.name; 
  const rollNumber = inputData.rollNumber;

  fs.readFile('output.json', 'utf8', (err, data) => {
    if (err) {
      console.error('Error reading JSON file:', err);
      return res.status(500).send('Error reading JSON file');
    }

    let jsonData;
    try {
      jsonData = JSON.parse(data);
    } catch (err) {
      console.error('Error parsing JSON data:', err);
      return res.status(500).send('Error parsing JSON data');
    }
    let correctCount = 0;

    for (const entry of jsonData) {
      const id = entry.id;
      const numbers = inputData[id];
      const sortedNumbers = numbers.split(",")
      const result = [];
      const strippedArr = sortedNumbers.map(str => str.trim());
      console.log(sortedNumbers);

      for (const item of strippedArr) {
        try {
          const fraction = new Fraction(item);
          result.push(fraction.valueOf());
        } catch (error) {
          result.push(Number(item));
        }
      }

      const result1 = result.map(Number).sort((a, b) => a - b);
      const fractions = [];

      for (const decimal of result1) {
        const fraction = new Fraction(decimal);
        fractions.push(fraction.toFraction());
      }
      console.log(result);
      console.log(fractions);


      const sortedString = fractions.join(", ");
      console.log(numbers, sortedString)

      const answer = sortedString
      const expectedAnswer = entry.answer;


      if (expectedAnswer && answer === expectedAnswer) {
        correctCount++;
      }
    }

    const totalQuestions = jsonData.length;
    const score = `${correctCount}/${totalQuestions}`;


    // Render the result EJS file with the score
    res.render('result', { score, name, rollNumber });
  });
});

app.get('/', (req, res) => {
  res.render('canvas');

});

app.post('/save', (req, res) => {
  const dataURL = req.body.dataURL;

  // Remove the data URL prefix
  const base64Data = dataURL.replace(/^data:image\/\w+;base64,/, '');

  // Generate a unique file name
  const fileName = `saved_images/image_${Date.now()}.jpg`;

  // Save the data as a PNG image
  fs.writeFile(fileName, base64Data, 'base64', (err) => {
    if (err) {
      console.error(err);
      res.sendStatus(500);
    } else {
      console.log(`Image saved as ${fileName}`);
      res.sendStatus(200);
    }
  });
});

app.post('/solve', (req, res) => {
  const dataURL = req.body.dataURL;
  console.log(dataURL)
  // Remove the data URL prefix
  const base64Data = dataURL.replace(/^data:image\/\w+;base64,/, '');

  // Generate a unique file name
  const fileName = `saved_images/image_${Date.now()}.jpg`;

  // Save the data as a PNG image
  fs.writeFile(fileName, base64Data, 'base64', (err) => {
    if (err) {
      console.error(err);
      res.sendStatus(500);
    } else {
      console.log(`Image saved as ${fileName}`);
      res.sendStatus(200);
      // code to solve single image
      axios.post('http://127.0.0.1:5000/solve', { dataURL })
        .then(response => {
          console.log(response.data.Equation);
          
        })
        .catch(error => {
          console.error(error);
        });




    }
  });
});

app.get('/output', (req, res) => {
  // Read the JSON file
  const jsonData = fs.readFileSync('output.json', 'utf8');
  let entries
  // const entries = JSON.parse(jsonData);
  if (jsonData.length === 0) {
    // JSON file is empty, return 0
    console.log('JSON file is empty');
    return res.render('output', { entries: 0 });
  }
  else {

    try {
      entries = JSON.parse(jsonData);
      return res.render('output', { entries });
    } catch (error) {
      console.error('Error parsing JSON:', error);

    }

  }
});

app.post('/upload', upload.single('image'), function (req, res, next) {
  // Access the uploaded file information
  const file = req.file;
  const equ = req.body.equation
  // console.log(req.body.equation)

  // Check if a file was uploaded
  if (!file) {
    res.status(400).send('No file uploaded.');
    return;
  }

  // Move the file to a desired location using fs.rename
  const oldPath = file.path;
  const newPath = 'uploads/' + file.originalname;

  fs.rename(oldPath, newPath, function (err) {
    if (err) {
      console.error(err);
      res.status(500).send('Error while saving the file.');
      return;
    }

    // res.send('File uploaded and saved successfully.');
  });
  axios.post('http://127.0.0.1:5000', { newPath, equ })
    .then(response => {
      // console.log(response.data);
      if (equ === "single"){
        return res.render('single', { entry: response.data });
      }
      res.redirect("/output")
    })
    .catch(error => {
      console.error(error);
    });

});





app.listen(port, () => {
  console.log(`Server running on http://localhost:${port}`);
});
