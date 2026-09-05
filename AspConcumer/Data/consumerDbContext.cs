using AspConcumer.Models;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection.Emit;
using System.Text;
using System.Threading.Tasks;

namespace consumer.Data
{
    public class consumerDbContext : DbContext
    {
        public consumerDbContext() { }
        public consumerDbContext(DbContextOptions options) : base(options) { }
        public DbSet<Surveys> peoples => Set<Surveys>();
        protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
        {
            if (!optionsBuilder.IsConfigured)
            {
                var connectionString = "Server=localhost;Port=3306;Database=kafka-db;Uid=root;Pwd=root;"; // עדכן את שם המסד אם צריך
                optionsBuilder.UseMySql(connectionString, ServerVersion.AutoDetect(connectionString));
            }
        }
        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);
            modelBuilder.Entity<Surveys>()
                .HasKey(a => a.ResponseId);
        }

    }
}
