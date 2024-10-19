const fs = require("fs");

function maxCalories(elf_file) {
    let calories = [];
    let elf_calories = 0;
    let max_calories = 0;
    let max_elf = 0;
    let elf = 0;
    let lineReader = require('readline').createInterface({
        input: require('fs').createReadStream(elf_file)
    });
    lineReader.on('line', function (line) {
        if (line == "") {
            elf++;
            if (elf_calories > max_calories) {
                max_calories = elf_calories;
                max_elf = elf;
            }
            elf_calories = 0;
        } else {
            elf_calories += parseInt(line);
        }
    });
    lineReader.on('close', function () {
        console.log("Elf " + max_elf + " has the most calories: " + max_calories);
    });
}

function sumOfCalories(elf_file) {
    let calories = fs.readFileSync(elf_file, 'utf8').split('\n');
    let calories_array = [];
    let sum = 0;
    for (let i = 0; i < calories.length; i++) {
        if (calories[i] == '') {
            calories_array.push(sum);
            sum = 0;
        } else {
            sum += parseInt(calories[i]);
        }
    }
    calories_array.push(sum);
    calories_array.sort((a, b) => b - a);
    return calories_array[0] + calories_array[1] + calories_array[2];
}
  
console.log(sumOfCalories('d1.txt'));