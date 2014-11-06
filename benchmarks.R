library(stats)

# using simple twisted alone tw2 branch
number_seqs <- c(2, 49,  64, 99, 199)
time <- c(    9.8, 105, 106, 98, 132)
plot(time ~ number_seqs, main="Bold_retriever: speed improvements of code", xlab="number of sequences", 
     ylab="processing time (seconds)", 
     type="l", col="black",
     lwd="2", xlim=c(0,200), las=1, ylim=c(0,200))
fit <- lm(time ~ number_seqs)


# no_threads
number_seqs <- c(1,     2,     4,     8,     16, 32, 64)
time <- c( 11.695, 14.804, 23.96, 36.28, 65.195,174,743)
lines(time ~ number_seqs, col="red", lwd="2")
fit <- lm(time ~ number_seqs)
# constant 5.14
#abline(lsfit(number_seqs, time))


legend(90,185,c("No Twisted", "With Twisted"), col=c(2,1), lty=c(1,1),
       lwd=c(2,2))

