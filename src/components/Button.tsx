import React from 'react';

interface IButton {
    text: string
    onClick: () => void
    disabled: boolean
}

const Button = (props: IButton) => {
    return (
        <button
            disabled={props.disabled}
            className='bg-blue-200 hover:bg-blue-300 disabled:hover:bg-gray-200 disabled:bg-gray-200 rounded-lg px-6 py-1 text-sm text-gray-700 disabled'
            onClick={props.onClick}>
            {props.text}
        </button>
    );
};

export default Button;
