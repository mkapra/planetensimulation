import { Animal } from '../models/Animal'
import AnimalRow from './AnimalRow';

interface IBoard {
    columns: number,
    rows: number,
    animals: Animal[][],
}

const Board = (props: IBoard) => {
    return (
        <div className="flex flex-col space-y-1 justify-center items-center">
            {props.animals.map((animalRow, index) => <AnimalRow animals={animalRow} key={`row-${index}`} />)}
        </div>
    );
};

export default Board;
