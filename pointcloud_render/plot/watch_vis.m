acc = csvread('./visual_csv/fork_accelerator.csv');
gryo= csvread('./visual_csv/fork_gryoscope.csv');
ori = csvread('./visual_csv/fork_orientation.csv');
acc_fig= figure(); gryo_fig= figure(); ori_fig= figure();

%% plot acceletor
figure(acc_fig);

x = 1:length(acc);
plot(x, acc(:,1), 'LineWidth',2);
hold on;
plot(x, acc(:,2), 'LineWidth',2);
hold on;
plot(x, acc(:,3), 'LineWidth',2);
hold on;
title('Accelerometer');
set(gca,'FontSize',20);
ylabel('$m/s^{2}$','FontSize',20,'Interpreter','latex');
xlabel('Sample','FontSize',15);
legend('x','y','z','Interpreter','latex');

%% plot gryoscope
figure(gryo_fig);
x = 1:length(gryo);
plot(x, gryo(:,1), 'LineWidth',2);
hold on;
plot(x, gryo(:,2), 'LineWidth',2);
hold on;
plot(x, gryo(:,3), 'LineWidth',2);
hold on;
title('Gryoscope');
set(gca,'FontSize',20);
ylabel('radians/sec','FontSize',15);
xlabel('Sample','FontSize',15);
legend('x','y','z','Interpreter','latex');

%% plot orientation
figure(ori_fig);
x = 1:length(ori);
plot(x, ori(:,1), 'LineWidth',2);
hold on;
plot(x, ori(:,2), 'LineWidth',2);
hold on;
plot(x, ori(:,3), 'LineWidth',2);
hold on;
plot(x, ori(:,4), 'LineWidth',2);
hold on;
title('Orientation');
set(gca,'FontSize',20);
xlabel('Sample','FontSize',15);
legend('scalar','x','y','z','Interpreter','latex');
%%


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
set(gca,'FontSize',15);


set(gcf, 'WindowStyle', 'normal');
set(gca, 'Unit', 'inches');
set(gca, 'Position', [.65 .65 4.6 3.125]);
set(gcf, 'Unit', 'inches');
set(gcf, 'Position', [0.25 2.5 5.5 4.05]);