import { Animal } from './Animal'

export class Shark extends Animal {
    getColor() {
        return "bg-red-400"
    };

    step(animals: Animal[][]) {
        return []
    }
}