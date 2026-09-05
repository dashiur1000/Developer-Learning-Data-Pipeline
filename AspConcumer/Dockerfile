FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build
WORKDIR /src

COPY ["AspConcumer.csproj", "./"]
RUN dotnet restore "AspConcumer.csproj"

COPY . .
RUN dotnet publish "AspConcumer.csproj" -c Release -o /app/publish

FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS runtime
WORKDIR /app
COPY --from=build /app/publish .

ENTRYPOINT ["dotnet", "AspConcumer.dll"]