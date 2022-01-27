import { Animal } from './Animal'

export class Empty extends Animal {
    getColor() {
        return "bg-blue-400"
    };

    step(animals: Animal[][]) {
        return []
    }
}