import React from 'react';

import { Animal } from '../models/Animal';
import AnimalView from './AnimalView';

interface IAnimalRow {
    animals: Animal[];
}

const AnimalRow = (props: IAnimalRow) => {
    return (
        <div className="flex space-x-1">
            {props.animals.map((animal, index) => {
                return <AnimalView color={animal.getColor()} key={index} />
            })}
        </div>
    );
};

export default AnimalRow;
