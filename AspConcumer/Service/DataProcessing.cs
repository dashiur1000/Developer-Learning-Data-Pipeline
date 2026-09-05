using System.Text.Json;
using AspConcumer.Models;
using MongoDB.Driver;

namespace AspConcumer.Service
{
    public class DataProcessing
    {
        private readonly IMongoDatabase _database;
        public DataProcessing(IMongoDatabase database)
        {
            _database = database;
        }
        public async Task<bool> FromTopicToDb(string model)
        {
            var c = JsonSerializer.Deserialize<Surveys>(model);
            if (c == null || string.IsNullOrEmpty(c.ResponseId))
            {
                return false;
            }
            var collection = _database.GetCollection<Surveys>("Surveys");
            var filter = Builders<Surveys>.Filter.Eq(s => s.ResponseId, c.ResponseId);

            var options = new ReplaceOptions { IsUpsert = true };

            await collection.ReplaceOneAsync(filter, c, options);
            return true;
        }
    }
}
