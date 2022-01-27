interface IAnimal {
    color: string,
}

const AnimalView = (props: IAnimal) => {
    return <div className={`${props.color} w-4 h-4 border-2 border-gray-500`} ></div >;
};

export default AnimalView;
