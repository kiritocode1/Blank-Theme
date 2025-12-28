/**
 * Syntax Highlighting Test File
 * This file contains various JavaScript and TypeScript constructs
 * to test editor themes.
 * @abstract 
 */

// 1. Primitive Types
const str: string = "Hello, World!";
const multilineStr: string = `
  This is a template literal
  with embedded expression: ${1 + 1}
`;
const num: number = 42;
const float: number = 3.14159;
const hex: number = 0xFF;
const bin: number = 0b1010;
const oct: number = 0o744;
const isTrue: boolean = true;
const isFalse: boolean = false;
const nll: null = null;
const und: undefined = undefined;
const sym: symbol = Symbol("sym");
const bigIntVal: bigint = 9007199254740991n;

const mathCalc = Math.max(1, 2, 3);
const jsonStr = JSON.stringify({ a: 1 });

// 2. Enums
enum Color {
    Red = "RED",
    Green = "GREEN",
    Blue = "BLUE",
}

// 3. Interfaces & Types
interface User {
    readonly id: number;
    name: string;
    email?: string; // Optional
    role: "admin" | "user" | "guest";
    tags: string[];
}

type ID = string | number;

// 4. Classes & Inheritance
abstract class Animal {
    constructor(public name: string) { }
    abstract makeSound(): void;
}

class Dog extends Animal {
    static species: string = "Canis lupus familiaris";
    private _age: number = 0;

    constructor(name: string, age: number) {
        super(name);
        this._age = age;
    }

    get age(): number {
        return this._age;
    }

    set age(value: number) {
        if (value < 0) throw new Error("Age cannot be negative");
        this._age = value;
    }


    makeSound(): void {
        console.log(`${this.name} barks!`);
    }

    async fetch(): Promise<string> {
        return new Promise((resolve) => {
            setTimeout(() => resolve("stick"), 1000);
        });
    }
}

// 5. Decorators (Experimental Syntax - Mock)
// Note: Actual decorator signature depends on TS version and configuration
function logMethod(target: any, propertyKey: string, descriptor: PropertyDescriptor) {
    const originalMethod = descriptor.value;
    descriptor.value = function (...args: any[]) {
        console.log(`Calling ${propertyKey} with`, args);
        return originalMethod.apply(this, args);
    };
}

// 6. Functions & Generics
function identity<T>(arg: T): T {
    return arg;
}

const arrowFunc = (x: number, y: number): number => x + y;

// 7. Object Literals & Destructuring
const config = {
    env: "development",
    port: 8080,
    db: {
        host: "localhost",
        password: "secret_password",
    },
    start() {
        console.log("Starting...");
    }
};

const { env, port } = config;
const [first, ...rest] = [1, 2, 3, 4];

// 8. Control Flow
function controlFlowDemo(val: number) {
    // TODO: Implement better logic here
    if (val > 10) {
        console.log("Big");
    } else if (val < 5) {
        console.log("Small");
    } else {
        console.log("Medium");
    }

    /* FIXME: precise handling */
    switch (val) {
        case 1:
            console.log("One");
            break;
        default:
            console.log("Other");
    }

    for (let i = 0; i < 5; i++) {
        continue;
    }

    const list = [1, 2, 3];
    for (const item of list) {
        if (item === 2) break;
    }
}

// 9. Error Handling
try {
    throw new Error("Something went wrong");
} catch (e: any) {
    const msg = e instanceof Error ? e.message : "Unknown error";
    console.error(msg);
} finally {
    console.log("Cleanup");
}

// 10. Regex
const emailRegex = /^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,6}$/g;
const match = "test@example.com".match(emailRegex);

// 11. Async/Await
async function fetchData(): Promise<void> {
    try {
        const result = await Promise.resolve("data");
        console.log(result);
    } catch (error) {
        console.error("Fetch error", error);
    }
}

// 12. Operators
const nested = config?.db?.host ?? "127.0.0.1";
const ternary = isTrue ? "Yes" : "No";

// 13. Modules (Mock)
export const VERSION = "1.0.0";
// import * as fs from 'fs'; // Uncomment to test module imports if types exist

export namespace Utils {
    export function log(msg: string) { console.log(msg); }
}
