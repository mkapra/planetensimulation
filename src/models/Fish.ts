import { Animal } from './Animal'
import { Empty } from './Empty'

export class Fish extends Animal {
    getColor() {
        return "bg-green-400"
    };

    step(animals: Animal[][]) {
        console.log("Calculating next step for fish", this)
        // Check if there is an empty space around the fish.
        let possibleMoves = [];

        if (animals[(this.y - 1 + animals.length) % animals.length][this.x % animals[0].length] instanceof Empty) {
            possibleMoves.push({ x: this.x, y: (this.y - 1 + animals.length) % animals.length })
        }
        if (animals[(this.y + 1) % animals.length][this.x % animals[0].length] instanceof Empty) {
            possibleMoves.push({ x: this.x, y: (this.y + 1) % animals.length })
        }
        if (animals[this.y % animals.length][(this.x + 1) % animals[0].length] instanceof Empty) {
            possibleMoves.push({ x: (this.x + 1) % animals[0].length, y: this.y })
        }
        if (animals[this.y % animals.length][(this.x - 1 + animals[0].length) % animals[0].length] instanceof Empty) {
            possibleMoves.push({ x: (this.x - 1 + animals[0].length) % animals[0].length, y: this.y })
        }

        // Check if the fish is at a border. If so, it can move to the other side.
        console.log(`Possible moves (${this.x}, ${this.y}):`, possibleMoves);

        console.log(`Animals before fish step (${this.x}, ${this.y}):`, animals);
        // If there are possible moves, pick one at random and move to that position
        if (possibleMoves.length > 0) {
            // reset the position of the animal to the new position
            let newPosition = possibleMoves[Math.floor(Math.random() * possibleMoves.length)];
            // store old positions
            let oldX = this.x;

            let oldY = this.y;

            // Map the old position to an empty space and the new position to a fish
            const newAnimals: Animal[][] = animals.map(row => row.map(animal => {
                // console.log(`Animal (${animal.x}, ${animal.y})`, animal);
                // If the animal is at the old position, replace it with an empty space
                if (animal.x === oldX && animal.y === oldY) {
                    return new Empty(oldX, oldY);
                }
                // If the animal is at the new position, replace it with a fish
                if (animal.x === newPosition.x && animal.y === newPosition.y) {
                    return this;
                }
                // Otherwise, return the animal
                return animal;
            }));

            // set new position
            this.x = newPosition.x;
            this.y = newPosition.y;
            console.log(`Fish moved from (${oldX}, ${oldY}) to (${this.x}, ${this.y})`);

            console.log(`Animals after fish step (${this.x}, ${this.y}):`, newAnimals);
            return newAnimals
        }

        return animals;
    }
}