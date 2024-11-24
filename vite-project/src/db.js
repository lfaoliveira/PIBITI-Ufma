
// classe e funções de wrapper pro indexedDB (suport total em todos os browsers grandes);

class BaseDados {
  constructor(dbName, storeName) {
    this.dbName = dbName;
    this.storeName = storeName;
    this.db = null;
  }

  // Open or initialize the database
  async open() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, 1);

      request.onupgradeneeded = (event) => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains(this.storeName)) {
          db.createObjectStore(this.storeName, { keyPath: "id", autoIncrement: true });
        }
      };

      request.onsuccess = (event) => {
        this.db = event.target.result;
        resolve(this.db);
      };

      request.onerror = (event) => {
        reject(`Error opening database: ${event.target.errorCode}`);
      };
    });
  }

  // Add data to the store
  async add(data) {
    await this.open();
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([this.storeName], "readwrite");
      const store = transaction.objectStore(this.storeName);
      const request = store.add(data);

      request.onsuccess = () => resolve(request.result); // Return the ID of the new record
      request.onerror = (event) => reject(`Add operation failed: ${event.target.errorCode}`);
    });
  }

  // Get data by ID
  async get(id) {
    await this.open();
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([this.storeName], "readonly");
      const store = transaction.objectStore(this.storeName);
      const request = store.get(id);

      request.onsuccess = () => resolve(request.result);
      request.onerror = (event) => reject(`Get operation failed: ${event.target.errorCode}`);
    });
  }

  // Get all data
  async getAll() {
    await this.open();
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([this.storeName], "readonly");
      const store = transaction.objectStore(this.storeName);
      const request = store.getAll();

      request.onsuccess = () => resolve(request.result);
      request.onerror = (event) => reject(`GetAll operation failed: ${event.target.errorCode}`);
    });
  }

  // Update data by ID
  async update(id, updatedData) {
    await this.open();
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([this.storeName], "readwrite");
      const store = transaction.objectStore(this.storeName);
      const getRequest = store.get(id);

      getRequest.onsuccess = () => {
        const data = { ...getRequest.result, ...updatedData };
        const putRequest = store.put(data);

        putRequest.onsuccess = () => resolve(true);
        putRequest.onerror = (event) => reject(`Update operation failed: ${event.target.errorCode}`);
      };

      getRequest.onerror = (event) => reject(`Failed to retrieve data for update: ${event.target.errorCode}`);
    });
  }

  // Delete data by ID
  async delete(id) {
    await this.open();
    return new Promise((resolve, reject) => {
      const transaction = this.db.transaction([this.storeName], "readwrite");
      const store = transaction.objectStore(this.storeName);
      const request = store.delete(id);

      request.onsuccess = () => resolve(true);
      request.onerror = (event) => reject(`Delete operation failed: ${event.target.errorCode}`);
    });
  }
}


export default BaseDados;
