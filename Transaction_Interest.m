function Transaction_Interest
    filename1 = 'Multipler Percentage 1 - 99 & Fees.xlsx';  
    filename2 = 'Number of Transactions.xlsx';  
    Interest =  xlsread(filename1,'Sheet1','C2:C4852');
    Transactions = xlsread(filename2,'Sheet1','C2:C4852');
    
    figure;
    hold on;
    ylabel('Number of Transactions')
    xlabel('Yield Rate')
    title('Yield Rates with Respect to Transaction Count')
    X = Interest;
    Y = Transactions;
    for i= length(Interest):-1: 1
        if Interest(i) == -100
            X(i) = [];
            Y(i) = [];
        end 
    end
    p = polyfit(X, Y, 1);
    slope = p(1);   
    scatter(X,Y)
    corr(X,Y)
    hold off;
    fig = gcf;
fig.PaperPositionMode = 'auto';
print('TransactionInterest','-dpng','-r300') 
    
    
end