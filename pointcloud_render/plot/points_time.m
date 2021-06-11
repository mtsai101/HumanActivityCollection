drink = csvread('./drink.csv');
idle = csvread('./idle.csv');

x = 1:length(idle);
plot(x, idle);
hold on;
x = 1:length(drink);
plot(x, drink);
hold on;

ylim([1,50]);
xlim([1,887]);

set(gca,'FontSize',20);
ylabel('Point Cloud #','FontSize',15);
xlabel('Frame','FontSize',15);
legend('Sit','Drink','Interpreter','latex');

a = get(gca,'XTickLabel');
set(gca,'XTickLabel',a,'fontsize',18);
set(gca, 'FontName', 'Times New Roman');
set(gca,'TickDir','out');

set(get(gca, 'xlabel'), 'interpreter', 'latex');
set(get(gca, 'xlabel'), 'FontName', 'Times New Roman');
set(get(gca, 'xlabel'), 'FontSize', 20);

set(get(gca, 'ylabel'), 'interpreter', 'latex');
set(get(gca, 'ylabel'), 'FontName', 'Times New Roman');
set(get(gca, 'ylabel'), 'FontSize', 20);


set(legend(), 'FontName', 'Times New Roman');
set(legend(), 'FontSize',12);


set(gcf, 'WindowStyle', 'normal');
set(gca, 'Unit', 'inches');
set(gca, 'Position', [.65 .65 4.6 3.125]);
set(gcf, 'Unit', 'inches');
set(gcf, 'Position', [0.25 2.5 5.5 4.05]);