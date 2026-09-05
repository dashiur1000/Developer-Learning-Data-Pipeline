using AspConcumer.Service;
using Confluent.Kafka;
using consumer.Data;
using Microsoft.EntityFrameworkCore;
using Microsoft.Extensions.DependencyInjection;
using MongoDB.Driver;

namespace Consumer;

class Program
{
    static async Task Main(string[] args)
    {
        var connectionString = "mongodb://db:27017";
        var databaseName = "my-database";

        var services = new ServiceCollection();

        services.AddSingleton<IMongoClient>(new MongoClient(connectionString));
        services.AddScoped(p => p.GetRequiredService<IMongoClient>().GetDatabase(databaseName));

        services.AddScoped<DataProcessing>();
        var serviceProvider = services.BuildServiceProvider();

        var bootstrap = "kafka:9092";
        var group = "vi-1";

        var consumerConfig = new ConsumerConfig
        {
            GroupId = group,
            BootstrapServers = bootstrap,
            AutoOffsetReset = AutoOffsetReset.Earliest,
            EnableAutoCommit = false
        };

        using var consumer = new ConsumerBuilder<Ignore, string>(consumerConfig).Build();
        consumer.Subscribe("processed-topic");
        while (true)
        {
            var result = consumer.Consume(TimeSpan.FromSeconds(20));
            if (result == null)
            {
                continue;
            }
            using var scope = serviceProvider.CreateAsyncScope();
            var processing = scope.ServiceProvider.GetRequiredService<DataProcessing>();
            if (await processing.FromTopicToDb(result.Message.Value))
            {
                consumer.Commit(result);
            }
        }
    }
}