FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY ["AiFromMongoAPI.csproj", "./"]
RUN dotnet restore "AiFromMongoAPI.csproj"

COPY . .
RUN dotnet publish "AiFromMongoAPI.csproj" -c Release -o /app/publish /p:UseAppHost=false

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS final
WORKDIR /app
EXPOSE 8080
EXPOSE 8081

COPY --from=build /app/publish .

ENTRYPOINT ["dotnet", "AiFromMongoAPI.dll"]