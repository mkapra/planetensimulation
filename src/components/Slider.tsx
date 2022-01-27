import React from 'react';

interface ISlider {
    min: number,
    max: number,
    value: number,
    setValue: (value: number) => void
}

const Slider = (props: ISlider) => {
    return (
        <div className="flex">
            <input
                className="w-2/3 m-4"
                type="range"
                min={props.min}
                max={props.max}
                value={props.value}
                onChange={(e) => props.setValue(parseInt(e.target.value))}
            />

            <p className="text-sm text-gray-600">{props.value}</p>
        </div>
    );
};

export default Slider;
