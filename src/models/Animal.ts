export abstract class Animal {
    x: number;
    y: number;

    constructor(x: number, y: number) {
        this.x = x;
        this.y = y;
    }
    abstract getColor(): string;
    abstract step(animals: Animal[][]): Animal[][];
}