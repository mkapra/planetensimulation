import { useEffect, useState } from "react";
import './App.css';

import { Animal } from './models/Animal'
import { Shark } from './models/Shark'
import { Fish } from './models/Fish'
import { Empty } from './models/Empty'

import Button from './components/Button';
import Navbar from './components/Navbar'
import Board from './components/Board'
import Slider from "./components/Slider";
import PopulationVisualisation from "./components/PopulationVisualisation";

function App() {
  const ys = 5;
  const xs = 5;

  let [animals, setAnimals] = useState<Animal[][]>([]);
  let [sharkCount, setSharkCount] = useState(0);
  let [fishCount, setFishCount] = useState(0);

  let [startAmountFishes, setStartAmountFishes] = useState(2);
  let [startAmountSharks, setStartAmountSharks] = useState(1);
  let [fishCountHistory, setFishCountHistory] = useState([startAmountFishes]);
  let [sharkCountHistory, setSharkCountHistory] = useState([startAmountSharks]);

  const generateAnimals = (amountFishes: number, amountSharks: number) => {
    setFishCountHistory([])
    setSharkCountHistory([])

    const generatedAnimals: Animal[][] = [];
    // Initialize array with empty cells
    for (var i: number = 0; i < ys; i++) {
      generatedAnimals[i] = [];
      for (var j: number = 0; j < xs; j++) {
        generatedAnimals[i][j] = new Empty(j, i);
      }
    }

    // Place fishes at random positions
    for (let i = 0; i < amountFishes; i++) {
      let x = Math.floor(Math.random() * xs)
      let y = Math.floor(Math.random() * ys)

      while (!(generatedAnimals[y][x] instanceof Empty)) {
        x = Math.floor(Math.random() * xs)
        y = Math.floor(Math.random() * ys)
      }

      generatedAnimals[y][x] = new Fish(x, y)
    }

    // Place sharks at random positions
    for (let i = 0; i < amountSharks; i++) {
      let y = Math.floor(Math.random() * ys)
      let x = Math.floor(Math.random() * xs)

      while (!(generatedAnimals[y][x] instanceof Empty)) {
        y = Math.floor(Math.random() * ys)
        x = Math.floor(Math.random() * xs)
      }

      generatedAnimals[y][x] = new Shark(x, y)
    }

    setAnimals(generatedAnimals)
  }

  const step = () => {
    const getFishes = () => {
      let fishes: Animal[] = [];
      for (let i = 0; i < animals.length; i++) {
        for (let j = 0; j < animals[i].length; j++) {
          if (animals[i][j] instanceof Fish) {
            fishes.push(animals[i][j])
          }
        }
      }
      return fishes;
    }

    const getSharks = () => {
      let sharks: Animal[] = [];
      for (let i = 0; i < animals.length; i++) {
        for (let j = 0; j < animals[i].length; j++) {
          if (animals[i][j] instanceof Shark) {
            sharks.push(animals[i][j])
          }
        }
      }
      return sharks;
    }

    getFishes().forEach(fish => setAnimals((previousAnimals) => fish.step([...previousAnimals])));
    getSharks();
  }

  // Counts the sharks and fishes in the world
  const countAnimals = (animals: Animal[][]) => {
    let fishes = 0;
    let sharks = 0;

    // Loop through all rows
    animals.forEach(row => {
      // Loop through all columns
      row.forEach(animal => {
        if (animal instanceof Fish) {
          fishes++;
        } else if (animal instanceof Shark) {
          sharks++;
        }
      })
    })

    // Return the amount of fishes and sharks
    return { fishes, sharks };
  }

  useEffect(() => {
    console.log("Animals changed!");
    // console.log("Animals:", animals);
    // Count animals
    const { fishes, sharks } = countAnimals(animals);
    // Set the amount of fishes and sharks
    setFishCount(fishes);
    setSharkCount(sharks);
    // Set the history of fishes and sharks
    setFishCountHistory(f => [...f, fishes]);
    setSharkCountHistory(s => [...s, sharks]);
  }, [animals])

  useEffect(() => {
    generateAnimals(startAmountFishes, startAmountSharks);
    setFishCountHistory([])
    setSharkCountHistory([])
  }, [startAmountFishes, startAmountSharks])

  return (
    <div className="App flex flex-col space-y-8">
      <Navbar />
      <div className="p-8">
        <div className='w-screen w-max-7xl flex mt-5'>
          <div className="w-1/2">
            <Board columns={xs} rows={ys} animals={animals} />
          </div>
          <div className="w-1/2 pl-4 space-y-4">
            <div className="flex space-x-4">
              <h1 className="text-2xl"><span className="font-bold">Fishes:</span> {fishCount}</h1>
              <h1 className="text-2xl"><span className="font-bold">Sharks:</span> {sharkCount}</h1>
            </div>
            <div className="flex space-x-4">
              <Button text={"Regenerate"} disabled={false} onClick={() => generateAnimals(startAmountFishes, startAmountSharks)} />
              <Button text={"Step"} disabled={sharkCount === 0 || fishCount === 0} onClick={() => {
                console.log("Step")
                step()
              }} />
              <Button text={"Run"} disabled={sharkCount === 0 || fishCount === 0} onClick={() => { }} />
              <Button text={"Stop"} disabled={sharkCount === 0 || fishCount === 0} onClick={() => { }} />
            </div>
            <div>
              <p>Amount of Fishes:</p>
              <Slider min={5} max={600} value={startAmountFishes} setValue={setStartAmountFishes} />
              <p>Amount of Sharks:</p>
              <Slider min={5} max={600} value={startAmountSharks} setValue={setStartAmountSharks} />
            </div>
          </div>
        </div>
        <div>
          <p>Visualization:</p>
          <PopulationVisualisation datasets={{
            // Array of a sequence from 1 to the amount of fishes
            labels: Array(fishCountHistory.length).fill(0).map((_, i) => i + 1),
            datasets: [
              {
                label: "Fishes",
                data: fishCountHistory,
                borderColor: 'rgb(53, 162, 235)',
                backgroundColor: 'rgba(53, 162, 235, 0.5)',
              },
              {
                label: "Sharks",
                data: sharkCountHistory,
                borderColor: 'rgb(255, 99, 132)',
                backgroundColor: 'rgba(255, 99, 132, 0.5)',
              }
            ]
          }} />
        </div>
      </div>
    </div>
  );
}

export default App;
