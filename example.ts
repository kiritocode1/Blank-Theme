const a  = 10; 


function blank(a: number , b :number){ 

    return a+b; 
}

class SomeClass{ 
    private some_priv_thing:number 

    public lol :number 

    constructor(){ 
        this.lol = 10;
        this.some_priv_thing = 22;
    }

    public getPrivThing(){ 
        return this.some_priv_thing;
    }
}


const someObj = new SomeClass();

console.log(someObj.getPrivThing());

