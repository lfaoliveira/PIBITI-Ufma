import { MongoClient } from "mongodb";

class DBManager{
    /* Classe de abstracao de detalhes do Banco de Dados */
    constructor(){
        const uriDB = "mongodb://localhost:<port>"
        this.client = new MongoClient(uriDB);
    }
    
    async connection(){
        
        try{
            await this.client.connect();
            return true;
        }
        catch(e) {
            console.error(e);
            return false;
        }
    }
    /**
     * @param {string} db
     * @param {string} collection
     * @param {Array} array
     */
    async insert(db, collection, array){
        const result = await this.client.db(db).collection(collection).insertMany(array);
        console.log(`ITENS INSERIDOS COM IDS: ${result.insertedIds}`);
    }
    async get(db, collection, id){
        const result = this.client.db(db).collection(collection).find(id);
    }
    //TODO: INSERIR FUNCOES DE UPDATE E DELETE
}


export default DBManager;
