using AiFromMongoAPI.Models;
using AiFromMongoAPI.Repositories;
using AiFromMongoAPI.Services;
using Microsoft.Extensions.Options;
using MongoDB.Driver;

var builder = WebApplication.CreateBuilder(args);

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.AddScoped<ISurveyRepository, SurveyRepository>();
builder.Services.Configure<DatabaseSettings>(builder.Configuration.GetSection("Surveys"));

builder.Services.AddSingleton<IMongoClient>(sp =>
{
    var options = sp.GetRequiredService<IOptions<DatabaseSettings>>().Value;

    if (string.IsNullOrWhiteSpace(options?.ConnectionString))
        throw new ArgumentException("Missing ConnectionString in 'Surveys' configuration.");

    return new MongoClient(options.ConnectionString);
});

builder.Services.AddScoped<IMongoDatabase>(sp =>
{
    var options = sp.GetRequiredService<IOptions<DatabaseSettings>>().Value;
    var client = sp.GetRequiredService<IMongoClient>();

    if (string.IsNullOrWhiteSpace(options?.DatabaseName))
        throw new ArgumentException("Missing DatabaseName in 'Surveys' configuration.");

    return client.GetDatabase(options.DatabaseName);
});

builder.Services.AddScoped<IMongoCollection<Surveys>>(sp =>
{
    var options = sp.GetRequiredService<IOptions<DatabaseSettings>>().Value;
    var database = sp.GetRequiredService<IMongoDatabase>();

    var collectionName = string.IsNullOrWhiteSpace(options.CollectionName) ? "Surveys" : options.CollectionName;
    return database.GetCollection<Surveys>(collectionName);
});

var app = builder.Build();

app.UseGlobalExceptionMiddleware();

app.UseSwagger();
app.UseSwaggerUI();
app.UseHttpsRedirection();
app.UseAuthorization();
app.MapControllers();

app.Run();