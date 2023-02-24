% Test synthetic topo functions

% x, y, positions
x = linspace(0, 100e3, 101);
y = linspace(0, 25e3, 101);
[xx, yy] = meshgrid(x, y);
xy = [xx(:), yy(:)];

% Mimic pin
pin.bed_elevation = @(xy, t) bed_elevation_synth(xy, t);

bed = bed_elevation_synth(xy, 0);
thick = ice_thickness_synth(xy, 0, pin);

bed = reshape(bed, size(xx));
thick = reshape(thick, size(xx));

figure;
subplot(2, 1, 1)
pcolor(xx, yy, bed)
axis image
shading flat
colorbar

subplot(2, 1, 2)
pcolor(xx, yy, thick)
axis image
shading flat
colorbar

